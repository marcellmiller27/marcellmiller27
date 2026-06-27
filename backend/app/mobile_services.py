import os
import time

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db_models import (
    DeviceCredentialDB,
    MembershipDB,
    OrganizationDB,
    SubscriptionDB,
    UserDB,
    UserSecurityDB,
    utc_now,
)
from app.foundation_models import (
    AuthResponse,
    Principal,
    SubscriptionPlan,
    SubscriptionStatus,
    UserRole,
)
from app.foundation_services import organization_read, subscription_read, user_read
from app.mobile_models import (
    BiometricChallengeResponse,
    BiometricRegisterResponse,
    DevCodeResponse,
    DeviceRead,
    Enable2FAResponse,
    LoginInitiateResponse,
    SecurityStatusResponse,
)
from app.security import (
    create_access_token,
    create_scoped_token,
    decode_scoped_token,
    decrypt_secret,
    encrypt_secret,
    generate_totp_secret,
    token_bytes_urlsafe,
    totp_now,
    totp_provisioning_uri,
    verify_password,
    verify_totp,
)


def _totp_plaintext(security: UserSecurityDB) -> str | None:
    """Return the decrypted TOTP secret for a security row (None if unset)."""
    if not security.totp_secret:
        return None
    return decrypt_secret(security.totp_secret)

TOTP_ISSUER = "John Henry Investments"
TOTP_PERIOD = 30


def is_dev_mode() -> bool:
    return os.getenv("APP_ENV", "development").lower() != "production"


# Backwards-compatible alias for internal callers.
_is_dev = is_dev_mode


class MobileAuthService:
    """Multi-factor sign-in flows for the mobile app (password, TOTP, biometric)."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def login_initiate(self, email: str, password: str) -> LoginInitiateResponse:
        user = self._authenticate(email, password)
        security = self._security_row(user.id)
        secret = _totp_plaintext(security)
        if security.two_factor_enabled and secret:
            challenge = create_scoped_token({"sub": user.id}, scope="2fa")
            return LoginInitiateResponse(
                status="two_factor_required",
                challenge_token=challenge,
                methods=["totp"],
                dev_code=totp_now(secret) if _is_dev() else None,
            )
        return LoginInitiateResponse(status="authenticated", auth=self._issue_auth(user))

    def two_factor_verify(self, challenge_token: str, code: str) -> AuthResponse:
        payload = decode_scoped_token(challenge_token, scope="2fa")
        user = self.db.get(UserDB, payload["sub"])
        if user is None or not user.is_active:
            raise ValueError("Account is no longer available.")
        security = self._security_row(user.id)
        secret = _totp_plaintext(security)
        # window=2 tolerates ~±60s of clock drift / manual entry latency.
        if not secret or not verify_totp(secret, code, window=2):
            raise ValueError("Invalid verification code.")
        return self._issue_auth(user)

    def current_dev_code(self, challenge_token: str) -> DevCodeResponse:
        """Dev-only: return the live TOTP code for a pending 2FA challenge.

        Mirrors an authenticator app that refreshes every period so the demo
        always shows a current code. Never exposed when APP_ENV=production.
        """
        payload = decode_scoped_token(challenge_token, scope="2fa")
        user = self.db.get(UserDB, payload["sub"])
        if user is None:
            raise ValueError("Account is no longer available.")
        security = self._security_row(user.id)
        secret = _totp_plaintext(security)
        if not secret:
            raise ValueError("Two-factor is not enabled.")
        return DevCodeResponse(
            code=totp_now(secret),
            seconds_remaining=TOTP_PERIOD - int(time.time()) % TOTP_PERIOD,
        )

    def enable_two_factor(self, principal: Principal) -> Enable2FAResponse:
        security = self._security_row(principal.user_id)
        secret = generate_totp_secret()
        security.totp_secret = encrypt_secret(secret)
        security.two_factor_enabled = True
        security.updated_at = utc_now()
        self.db.commit()
        return Enable2FAResponse(
            enabled=True,
            secret=secret,
            otpauth_url=totp_provisioning_uri(secret, principal.email, TOTP_ISSUER),
            current_code=totp_now(secret) if _is_dev() else None,
        )

    def disable_two_factor(self, principal: Principal) -> None:
        security = self._security_row(principal.user_id)
        security.two_factor_enabled = False
        security.totp_secret = None
        security.updated_at = utc_now()
        self.db.commit()

    def register_biometric(
        self,
        principal: Principal,
        credential_id: str,
        public_key: str | None,
        label: str,
    ) -> BiometricRegisterResponse:
        existing = self.db.scalar(
            select(DeviceCredentialDB).where(DeviceCredentialDB.credential_id == credential_id)
        )
        if existing is None:
            self.db.add(
                DeviceCredentialDB(
                    user_id=principal.user_id,
                    credential_id=credential_id,
                    public_key=public_key,
                    label=label or "Mobile device",
                )
            )
            self.db.commit()
        return BiometricRegisterResponse(
            registered=True,
            credential_id=credential_id,
            label=label or "Mobile device",
        )

    def biometric_challenge(self, email: str) -> BiometricChallengeResponse:
        user = self.db.scalar(select(UserDB).where(UserDB.email == email.lower().strip()))
        if user is None:
            return BiometricChallengeResponse(has_credential=False)
        credentials = self._devices(user.id)
        if not credentials:
            return BiometricChallengeResponse(has_credential=False)
        nonce = token_bytes_urlsafe(24)
        challenge = create_scoped_token({"sub": user.id, "nonce": nonce}, scope="biometric")
        return BiometricChallengeResponse(
            has_credential=True,
            challenge=nonce,
            challenge_token=challenge,
            credential_ids=[credential.credential_id for credential in credentials],
        )

    def biometric_assert(self, challenge_token: str, credential_id: str) -> AuthResponse:
        payload = decode_scoped_token(challenge_token, scope="biometric")
        user = self.db.get(UserDB, payload["sub"])
        if user is None or not user.is_active:
            raise ValueError("Account is no longer available.")
        credential = self.db.scalar(
            select(DeviceCredentialDB).where(
                DeviceCredentialDB.user_id == user.id,
                DeviceCredentialDB.credential_id == credential_id,
            )
        )
        if credential is None:
            raise ValueError("Unrecognized device credential.")
        credential.last_used_at = utc_now()
        self.db.commit()
        return self._issue_auth(user)

    def security_status(self, principal: Principal) -> SecurityStatusResponse:
        security = self._security_row(principal.user_id)
        devices = self._devices(principal.user_id)
        return SecurityStatusResponse(
            two_factor_enabled=security.two_factor_enabled,
            biometric_enabled=len(devices) > 0,
            device_count=len(devices),
            devices=[
                DeviceRead(
                    credential_id=device.credential_id,
                    label=device.label,
                    created_at=device.created_at,
                    last_used_at=device.last_used_at,
                )
                for device in devices
            ],
        )

    def _authenticate(self, email: str, password: str) -> UserDB:
        normalized = email.lower().strip()
        user = self.db.scalar(select(UserDB).where(UserDB.email == normalized))
        if user is None or not verify_password(password, user.password_hash):
            raise ValueError("Invalid email or password.")
        if not user.is_active:
            raise ValueError("User account is inactive.")
        return user

    def _security_row(self, user_id: str) -> UserSecurityDB:
        security = self.db.scalar(
            select(UserSecurityDB).where(UserSecurityDB.user_id == user_id)
        )
        if security is None:
            security = UserSecurityDB(user_id=user_id)
            self.db.add(security)
            self.db.flush()
        return security

    def _devices(self, user_id: str) -> list[DeviceCredentialDB]:
        return list(
            self.db.scalars(
                select(DeviceCredentialDB)
                .where(DeviceCredentialDB.user_id == user_id)
                .order_by(DeviceCredentialDB.created_at.desc())
            ).all()
        )

    def _issue_auth(self, user: UserDB) -> AuthResponse:
        membership = self.db.scalar(select(MembershipDB).where(MembershipDB.user_id == user.id))
        if membership is None:
            raise ValueError("User does not belong to an organization.")
        organization = self.db.get(OrganizationDB, membership.organization_id)
        subscription = self._current_subscription(organization.id)
        token = create_access_token(
            {
                "sub": user.id,
                "organization_id": organization.id,
                "role": membership.role,
                "email": user.email,
            }
        )
        return AuthResponse(
            access_token=token,
            user=user_read(user),
            organization=organization_read(organization),
            role=UserRole(membership.role),
            subscription=subscription_read(subscription),
        )

    def _current_subscription(self, organization_id: str) -> SubscriptionDB:
        subscription = self.db.scalar(
            select(SubscriptionDB).where(SubscriptionDB.organization_id == organization_id)
        )
        if subscription is None:
            subscription = SubscriptionDB(
                organization_id=organization_id,
                plan=SubscriptionPlan.CONSUMER.value,
                status=SubscriptionStatus.TRIALING.value,
                provider="stripe",
            )
            self.db.add(subscription)
            self.db.flush()
        return subscription
