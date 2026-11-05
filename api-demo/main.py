from fastapi import (
    FastAPI,
    UploadFile,
    File,
    BackgroundTasks,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from pathlib import Path
from uuid import uuid4

from database import engine, Base, get_db

from models import Invoice

from schemas import (
    InvoiceCreateResponse,
    InvoiceResponse,
    InvoiceResultResponse,
    InvoiceListResponse
)

from crud import (
    create_invoice,
    get_invoice,
    get_all_invoices
)

from services import process_invoice


# ==========================================
# APPLICATION SETUP
# ==========================================

app = FastAPI(
    title="Async Invoice Processing API",
    description="Database-backed Invoice Processing API",
    version="2.0.0"
)


# Create database tables if they do not exist
Base.metadata.create_all(bind=engine)


# Create uploads directory
UPLOAD_DIR = Path("uploads")

UPLOAD_DIR.mkdir(exist_ok=True)


# Supported file types
ALLOWED_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "application/pdf": ".pdf"
}


# ==========================================
# HEALTH CHECK
# ==========================================

@app.get("/")
def home():

    return {
        "message": "Welcome to Async Invoice Processing API",
        "status": "running"
    }


@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }


# ==========================================
# CREATE / UPLOAD INVOICE
# ==========================================

@app.post(
    "/invoices",
    status_code=202,
    response_model=InvoiceCreateResponse
)
async def upload_invoice(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    # Validate file type
    if file.content_type not in ALLOWED_TYPES:

        raise HTTPException(
            status_code=400,
            detail="Unsupported file type"
        )

    # Generate unique Job ID
    job_id = str(uuid4())

    # Generate safe filename
    extension = ALLOWED_TYPES[file.content_type]

    filename = f"{job_id}{extension}"

    file_path = UPLOAD_DIR / filename

    # Read uploaded file
    content = await file.read()

    if not content:

        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty"
        )

    # Save file locally
    with open(file_path, "wb") as f:
        f.write(content)

    try:

        # Create database record
        invoice = create_invoice(
            db=db,
            job_id=job_id,
            filename=filename
        )

    except Exception:

        # Remove uploaded file if database insertion fails
        file_path.unlink(missing_ok=True)

        raise HTTPException(
            status_code=500,
            detail="Failed to create invoice job"
        )

    # Schedule background processing
    background_tasks.add_task(
        process_invoice,
        job_id
    )

    return {
        "job_id": job_id,
        "status": invoice.status,
        "message": "Invoice submitted successfully"
    }


# ==========================================
# GET ALL INVOICE JOBS
# ==========================================

@app.get(
    "/invoices",
    response_model=InvoiceListResponse
)
def list_invoices(
    db: Session = Depends(get_db)
):

    invoices = get_all_invoices(db)

    return {
        "total": len(invoices),
        "invoices": invoices
    }


# ==========================================
# GET SPECIFIC INVOICE JOB
# ==========================================

@app.get(
    "/invoices/{job_id}",
    response_model=InvoiceResponse
)
def get_invoice_status(
    job_id: str,
    db: Session = Depends(get_db)
):

    invoice = get_invoice(
        db=db,
        job_id=job_id
    )

    if invoice is None:

        raise HTTPException(
            status_code=404,
            detail="Invoice job not found"
        )

    return invoice


# ==========================================
# GET INVOICE EXTRACTION RESULT
# ==========================================

@app.get(
    "/invoices/{job_id}/result",
    response_model=InvoiceResultResponse
)
def get_invoice_result(
    job_id: str,
    db: Session = Depends(get_db)
):

    invoice = get_invoice(
        db=db,
        job_id=job_id
    )

    if invoice is None:

        raise HTTPException(
            status_code=404,
            detail="Invoice job not found"
        )

    if invoice.status in ["pending", "processing"]:

        raise HTTPException(
            status_code=409,
            detail="Invoice is still being processed"
        )

    return {
        "job_id": invoice.job_id,
        "status": invoice.status,
        "result": invoice.result,
        "error": invoice.error
    }