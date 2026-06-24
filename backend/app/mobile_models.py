from datetime import datetime

from pydantic import BaseModel, Field

from app.foundation_models import AuthResponse


class LoginInitiateRequest(BaseModel):
    email: str
    password: str


class LoginInitiateResponse(BaseModel):
    """Step one of mobile sign-in.

    ``status`` is ``authenticated`` when no second factor is required (``auth``
    is populated), or ``two_factor_required`` when the client must complete a
    second step with ``challenge_token``.
    """

    status: str
    auth: AuthResponse | None = None
    challenge_token: str | None = None
    methods: list[str] = Field(default_factory=list)
    dev_code: str | None = None


class TwoFactorVerifyRequest(BaseModel):
    challenge_token: str
    code: str


class Enable2FAResponse(BaseModel):
    enabled: bool
    secret: str
    otpauth_url: str
    current_code: str | None = None


class SimpleStatusResponse(BaseModel):
    status: str
    message: str


class BiometricRegisterRequest(BaseModel):
    credential_id: str
    public_key: str | None = None
    label: str = "Mobile device"


class BiometricRegisterResponse(BaseModel):
    registered: bool
    credential_id: str
    label: str


class BiometricChallengeRequest(BaseModel):
    email: str


class BiometricChallengeResponse(BaseModel):
    has_credential: bool
    challenge: str | None = None
    challenge_token: str | None = None
    credential_ids: list[str] = Field(default_factory=list)


class BiometricAssertRequest(BaseModel):
    challenge_token: str
    credential_id: str
    signature: str | None = None


class DeviceRead(BaseModel):
    credential_id: str
    label: str
    created_at: datetime
    last_used_at: datetime | None = None


class SecurityStatusResponse(BaseModel):
    two_factor_enabled: bool
    biometric_enabled: bool
    device_count: int
    devices: list[DeviceRead] = Field(default_factory=list)
