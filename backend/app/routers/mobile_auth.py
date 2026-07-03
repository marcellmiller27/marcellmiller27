# JHI-SIG: 69M2705M | Identity, Auth & Security | John Henry Investments (proprietary)
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_principal
from app.foundation_models import AuthResponse, Principal
from app.mobile_models import (
    BiometricAssertRequest,
    BiometricChallengeRequest,
    BiometricChallengeResponse,
    BiometricRegisterRequest,
    BiometricRegisterResponse,
    DevCodeRequest,
    DevCodeResponse,
    Enable2FAResponse,
    LoginInitiateRequest,
    LoginInitiateResponse,
    SecurityStatusResponse,
    SimpleStatusResponse,
    TwoFactorVerifyRequest,
)
from app.mobile_services import MobileAuthService, is_dev_mode

router = APIRouter(prefix="/auth", tags=["mobile-auth"])


@router.post("/login/initiate", response_model=LoginInitiateResponse)
def login_initiate(
    payload: LoginInitiateRequest,
    db: Annotated[Session, Depends(get_db)],
) -> LoginInitiateResponse:
    try:
        return MobileAuthService(db).login_initiate(payload.email, payload.password)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc


@router.post("/2fa/verify", response_model=AuthResponse)
def two_factor_verify(
    payload: TwoFactorVerifyRequest,
    db: Annotated[Session, Depends(get_db)],
) -> AuthResponse:
    try:
        return MobileAuthService(db).two_factor_verify(payload.challenge_token, payload.code)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc


@router.post("/2fa/dev-code", response_model=DevCodeResponse)
def two_factor_dev_code(
    payload: DevCodeRequest,
    db: Annotated[Session, Depends(get_db)],
) -> DevCodeResponse:
    if not is_dev_mode():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not available.")
    try:
        return MobileAuthService(db).current_dev_code(payload.challenge_token)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc


@router.post("/2fa/enable", response_model=Enable2FAResponse)
def enable_two_factor(
    principal: Annotated[Principal, Depends(get_current_principal)],
    db: Annotated[Session, Depends(get_db)],
) -> Enable2FAResponse:
    return MobileAuthService(db).enable_two_factor(principal)


@router.post("/2fa/disable", response_model=SimpleStatusResponse)
def disable_two_factor(
    principal: Annotated[Principal, Depends(get_current_principal)],
    db: Annotated[Session, Depends(get_db)],
) -> SimpleStatusResponse:
    MobileAuthService(db).disable_two_factor(principal)
    return SimpleStatusResponse(status="ok", message="Two-factor authentication disabled.")


@router.post("/biometric/register", response_model=BiometricRegisterResponse)
def register_biometric(
    payload: BiometricRegisterRequest,
    principal: Annotated[Principal, Depends(get_current_principal)],
    db: Annotated[Session, Depends(get_db)],
) -> BiometricRegisterResponse:
    return MobileAuthService(db).register_biometric(
        principal, payload.credential_id, payload.public_key, payload.label
    )


@router.post("/biometric/challenge", response_model=BiometricChallengeResponse)
def biometric_challenge(
    payload: BiometricChallengeRequest,
    db: Annotated[Session, Depends(get_db)],
) -> BiometricChallengeResponse:
    return MobileAuthService(db).biometric_challenge(payload.email)


@router.post("/biometric/assert", response_model=AuthResponse)
def biometric_assert(
    payload: BiometricAssertRequest,
    db: Annotated[Session, Depends(get_db)],
) -> AuthResponse:
    try:
        return MobileAuthService(db).biometric_assert(payload.challenge_token, payload.credential_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc


@router.get("/security/status", response_model=SecurityStatusResponse)
def security_status(
    principal: Annotated[Principal, Depends(get_current_principal)],
    db: Annotated[Session, Depends(get_db)],
) -> SecurityStatusResponse:
    return MobileAuthService(db).security_status(principal)
