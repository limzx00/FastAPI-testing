from pydantic import BaseModel, ConfigDict
from typing import Optional, Any
from datetime import datetime


# Response when submitting an invoice
class InvoiceCreateResponse(BaseModel):

    job_id: str
    status: str
    message: str


# Response for invoice job information
class InvoiceResponse(BaseModel):

    job_id: str
    filename: Optional[str] = None
    status: str

    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Response containing extraction results
class InvoiceResultResponse(BaseModel):

    job_id: str
    status: str

    result: Optional[dict[str, Any]] = None

    error: Optional[str] = None


# Response when retrieving all jobs
class InvoiceListResponse(BaseModel):

    total: int
    invoices: list[InvoiceResponse]