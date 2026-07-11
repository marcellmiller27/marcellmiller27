from fastapi import APIRouter, HTTPException, status

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
from app.services import IntegrationService
from app.store import store

router = APIRouter(prefix="/integrations", tags=["integrations"])
integration_service = IntegrationService(store)


@router.get("/connectors", response_model=list[IntegrationConnector])
def list_connectors() -> list[IntegrationConnector]:
    return integration_service.connectors()


@router.post(
    "/connections",
    response_model=IntegrationConnection,
    status_code=status.HTTP_201_CREATED,
)
def create_connection(payload: IntegrationConnectionCreate) -> IntegrationConnection:
    try:
        return integration_service.create_connection(payload)
    except KeyError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/connections", response_model=list[IntegrationConnection])
def list_connections() -> list[IntegrationConnection]:
    return list(store.integration_connections.values())


@router.post("/sync-jobs", response_model=SyncJob, status_code=status.HTTP_201_CREATED)
def create_sync_job(payload: SyncJobCreate) -> SyncJob:
    try:
        return integration_service.create_sync_job(payload)
    except (KeyError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/sync-jobs", response_model=list[SyncJob])
def list_sync_jobs() -> list[SyncJob]:
    return list(store.sync_jobs.values())


@router.post(
    "/banking/transactions",
    response_model=BankingTransaction,
    status_code=status.HTTP_201_CREATED,
)
def import_banking_transaction(payload: BankingTransactionCreate) -> BankingTransaction:
    try:
        return integration_service.import_banking_transaction(payload)
    except KeyError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/banking/transactions", response_model=list[BankingTransaction])
def list_banking_transactions() -> list[BankingTransaction]:
    return list(store.banking_transactions.values())


@router.post("/vendor/bills", response_model=VendorBill, status_code=status.HTTP_201_CREATED)
def import_vendor_bill(payload: VendorBillCreate) -> VendorBill:
    try:
        return integration_service.import_vendor_bill(payload)
    except KeyError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/vendor/bills", response_model=list[VendorBill])
def list_vendor_bills() -> list[VendorBill]:
    return list(store.vendor_bills.values())


@router.post("/office/export-package", response_model=OfficeExportPackage)
def create_office_export_package(payload: OfficeExportRequest) -> OfficeExportPackage:
    return integration_service.office_export_package(payload)
