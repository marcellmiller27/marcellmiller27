# JHI-SIG: 69M2705M | Integrations API | John Henry Investments (proprietary)
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.integration_services import IntegrationService
from app.models import (
    BankingTransaction,
    BankingTransactionCreate,
    IntegrationConnection,
    IntegrationConnectionCreate,
    IntegrationConnector,
    OfficeExportPackage,
    OfficeExportRequest,
    SyncJob,
    SyncJobCreate,
    VendorBill,
    VendorBillCreate,
)

router = APIRouter(prefix="/integrations", tags=["integrations"])
integration_service = IntegrationService()


@router.get("/connectors", response_model=list[IntegrationConnector])
def list_connectors() -> list[IntegrationConnector]:
    return integration_service.connectors()


@router.post(
    "/connections",
    response_model=IntegrationConnection,
    status_code=status.HTTP_201_CREATED,
)
def create_connection(
    payload: IntegrationConnectionCreate, db: Annotated[Session, Depends(get_db)]
) -> IntegrationConnection:
    try:
        return integration_service.create_connection(db, payload)
    except KeyError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/connections", response_model=list[IntegrationConnection])
def list_connections(db: Annotated[Session, Depends(get_db)]) -> list[IntegrationConnection]:
    return integration_service.list_connections(db)


@router.post("/sync-jobs", response_model=SyncJob, status_code=status.HTTP_201_CREATED)
def create_sync_job(
    payload: SyncJobCreate, db: Annotated[Session, Depends(get_db)]
) -> SyncJob:
    try:
        return integration_service.create_sync_job(db, payload)
    except (KeyError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/sync-jobs", response_model=list[SyncJob])
def list_sync_jobs(db: Annotated[Session, Depends(get_db)]) -> list[SyncJob]:
    return integration_service.list_sync_jobs(db)


@router.post(
    "/banking/transactions",
    response_model=BankingTransaction,
    status_code=status.HTTP_201_CREATED,
)
def import_banking_transaction(
    payload: BankingTransactionCreate, db: Annotated[Session, Depends(get_db)]
) -> BankingTransaction:
    try:
        return integration_service.import_banking_transaction(db, payload)
    except KeyError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/banking/transactions", response_model=list[BankingTransaction])
def list_banking_transactions(
    db: Annotated[Session, Depends(get_db)]
) -> list[BankingTransaction]:
    return integration_service.list_banking_transactions(db)


@router.post("/vendor/bills", response_model=VendorBill, status_code=status.HTTP_201_CREATED)
def import_vendor_bill(
    payload: VendorBillCreate, db: Annotated[Session, Depends(get_db)]
) -> VendorBill:
    try:
        return integration_service.import_vendor_bill(db, payload)
    except KeyError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/vendor/bills", response_model=list[VendorBill])
def list_vendor_bills(db: Annotated[Session, Depends(get_db)]) -> list[VendorBill]:
    return integration_service.list_vendor_bills(db)


@router.post("/office/export-package", response_model=OfficeExportPackage)
def create_office_export_package(
    payload: OfficeExportRequest, db: Annotated[Session, Depends(get_db)]
) -> OfficeExportPackage:
    return integration_service.office_export_package(db, payload)
