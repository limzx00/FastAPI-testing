from fastapi import FastAPI, BackgroundTasks, HTTPException
from uuid import uuid4
import time

app = FastAPI()

# Temporary in-memory job storage
jobs = {}

def process_invoice(job_id: str):

    jobs[job_id]["status"] = "processing"

    # Simulate OCR processing
    time.sleep(10)

    # Simulate extracted invoice data
    jobs[job_id]["result"] = {
        "invoice_number": "INV-001",
        "vendor_name": "ABC Sdn Bhd",
        "total_amount": 1500.00
    }

    jobs[job_id]["status"] = "completed"


@app.post("/invoices", status_code=202)
def upload_invoice(background_tasks: BackgroundTasks):

    job_id = str(uuid4())

    jobs[job_id] = {
        "status": "pending",
        "result": None
    }

    background_tasks.add_task(
        process_invoice,
        job_id
    )

    return {
        "job_id": job_id,
        "status": "pending",
        "message": "Invoice submitted successfully"
    }


@app.get("/invoices/{job_id}")
def get_invoice_status(job_id: str):

    if job_id not in jobs:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    return {
        "job_id": job_id,
        **jobs[job_id]
    }