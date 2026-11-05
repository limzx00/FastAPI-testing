import time

from database import SessionLocal
from crud import (
    update_invoice_status,
    update_invoice_result,
    update_invoice_error
)


def process_invoice(job_id: str):

    # Create a NEW database session for the background task
    db = SessionLocal()

    try:

        print(f"Processing invoice: {job_id}")

        # Update status to processing
        update_invoice_status(
            db=db,
            job_id=job_id,
            status="processing"
        )

        # Simulate OCR processing
        time.sleep(10)

        # Simulated extraction result
        extracted_data = {
            "invoice_number": "INV-2026-001",
            "invoice_date": "2026-11-05",
            "vendor_name": "ABC Sdn Bhd",
            "vendor_address": "Kuala Lumpur, Malaysia",
            "total_amount": 1500.00,
            "currency": "MYR"
        }

        # Save extraction result
        update_invoice_result(
            db=db,
            job_id=job_id,
            result=extracted_data
        )

        print(f"Invoice completed: {job_id}")

    except Exception as e:

        db.rollback()

        update_invoice_error(
            db=db,
            job_id=job_id,
            error=str(e)
        )

        print(f"Invoice processing failed: {e}")

    finally:

        # Always close the database session
        db.close()