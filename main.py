from fastapi import FastAPI, UploadFile, File, HTTPException
from pathlib import Path
import uuid

app = FastAPI()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@app.post("/upload-invoice")
async def upload_invoice(file: UploadFile = File(...)):

    allowed_types = [
        "image/jpeg",
        "image/png",
        "application/pdf"
    ]

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type"
        )

    file_id = str(uuid.uuid4())

    extension = Path(file.filename).suffix.lower()

    file_path = UPLOAD_DIR / f"{file_id}{extension}"

    content = await file.read()

    with open(file_path, "wb") as f:
        f.write(content)

    return {
        "file_id": file_id,
        "filename": file.filename,
        "content_type": file.content_type,
        "file_size": len(content),
        "status": "uploaded"
    }