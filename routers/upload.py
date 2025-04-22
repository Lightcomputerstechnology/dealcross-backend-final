# File: routes/upload.py

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from typing import List
from starlette.status import HTTP_400_BAD_REQUEST
from utils.auth import get_current_user  # Token validation

router = APIRouter()

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "pdf"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def validate_file(file: UploadFile):
    # Check file extension
    ext = file.filename.split('.')[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type: .{ext}. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )

@router.post("/upload")
async def upload_file(file: UploadFile = File(...), user=Depends(get_current_user)):
    # Validate file type
    validate_file(file)
    
    # Validate file size
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"File too large. Max size is {MAX_FILE_SIZE // (1024 * 1024)}MB."
        )
    
    # [Placeholder for saving file to disk/cloud]
    
    return {"message": "File uploaded successfully."}
