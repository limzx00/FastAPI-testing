from sqlalchemy.orm import Session

from models import Invoice


# CREATE: Create a new invoice job
def create_invoice(
    db: Session,
    job_id: str,
    filename: str
):

    invoice = Invoice(
        job_id=job_id,
        filename=filename,
        status="pending"
    )

    db.add(invoice)

    db.commit()

    db.refresh(invoice)

    return invoice


# READ: Retrieve one invoice job
def get_invoice(
    db: Session,
    job_id: str
):

    return (
        db.query(Invoice)
        .filter(Invoice.job_id == job_id)
        .first()
    )


# READ: Retrieve all invoice jobs
def get_all_invoices(
    db: Session
):

    return (
        db.query(Invoice)
        .order_by(Invoice.created_at.desc())
        .all()
    )


# UPDATE: Update invoice processing status
def update_invoice_status(
    db: Session,
    job_id: str,
    status: str
):

    invoice = get_invoice(db, job_id)

    if invoice is None:
        return None

    invoice.status = status

    db.commit()

    db.refresh(invoice)

    return invoice


# UPDATE: Save invoice extraction result
def update_invoice_result(
    db: Session,
    job_id: str,
    result: dict
):

    invoice = get_invoice(db, job_id)

    if invoice is None:
        return None

    invoice.result = result
    invoice.status = "completed"
    invoice.error = None

    db.commit()

    db.refresh(invoice)

    return invoice


# UPDATE: Record processing failure
def update_invoice_error(
    db: Session,
    job_id: str,
    error: str
):

    invoice = get_invoice(db, job_id)

    if invoice is None:
        return None

    invoice.status = "failed"
    invoice.error = error

    db.commit()

    db.refresh(invoice)

    return invoice