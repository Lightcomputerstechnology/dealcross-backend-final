# File: admin_views/change_password_view.py

from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from fastapi_admin.depends import get_current_admin
from core.security import verify_password, get_password_hash
from models.user import User

router = APIRouter()

@router.get("/change-password")
async def change_password_form(request: Request, admin=Depends(get_current_admin)):
    return templates.TemplateResponse("change_password.html", {"request": request, "admin": admin})


@router.post("/change-password")
async def change_password_submit(
    request: Request,
    old_password: str = Form(...),
    new_password: str = Form(...),
    admin=Depends(get_current_admin)
):
    user = await User.get(id=admin.id)

    if not verify_password(old_password, user.password):
        return templates.TemplateResponse("change_password.html", {
            "request": request,
            "admin": admin,
            "error": "Old password is incorrect."
        })

    user.password = get_password_hash(new_password)
    await user.save()
    return RedirectResponse(url="/admin", status_code=HTTP_303_SEE_OTHER)# File: admin_views/change_password_view.py
from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi_admin.app import app
from fastapi_admin.depends import get_current_admin
from fastapi_admin.template import templates
from passlib.context import CryptContext
from starlette import status
from models.user import User

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.get("/change-password")
async def change_password_form(request: Request, admin=Depends(get_current_admin)):
    if not admin.is_superuser:
        return RedirectResponse("/admin", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("change_password.html", {"request": request})

@router.post("/change-password")
async def change_password_submit(
    request: Request,
    old_password: str = Form(...),
    new_password: str = Form(...),
    admin=Depends(get_current_admin)
):
    if not pwd_context.verify(old_password, admin.password):
        return templates.TemplateResponse("change_password.html", {
            "request": request,
            "error": "Incorrect current password."
        })

    hashed = pwd_context.hash(new_password)
    admin.password = hashed
    await admin.save()

    return templates.TemplateResponse("change_password.html", {
        "request": request,
        "success": "Password changed successfully."
    })