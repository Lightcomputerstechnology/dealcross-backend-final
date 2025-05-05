from fastapi import APIRouter, HTTPException
from schemas.contact import ContactRequest
from utils.email_sender import send_contact_email

router = APIRouter(prefix="/contact", tags=["Contact"])

@router.post("/send-email")
def send_email(contact: ContactRequest):
    try:
        send_contact_email(contact.name, contact.email, contact.message)
        return {"success": True, "message": "Email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to send email")