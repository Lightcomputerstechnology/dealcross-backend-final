# File: admin/widgets/change_password.py

from fastapi import Request, Form
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_302_FOUND
from fastapi_admin.widgets import inputs
from fastapi_admin.depends import get_current_admin
from passlib.context import CryptContext
from models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class ChangePasswordWidget:
    async def render(self, request: Request):
        return {
            "title": "Change Password",
            "inputs": [
                inputs.Password(name="old_password", label="Old Password"),
                inputs.Password(name="new_password", label="New Password"),
                inputs.Password(name="confirm_password", label="Confirm New Password"),
            ]
        }

    async def handle(self, request: Request):
        form = await request.form()
        old_password = form.get("old_password")
        new_password = form.get("new_password")
        confirm_password = form.get("confirm_password")

        admin_user: User = await get_current_admin(request)

        if not pwd_context.verify(old_password, admin_user.hashed_password):
            return {"error": "Old password is incorrect."}

        if new_password != confirm_password:
            return {"error": "New passwords do not match."}

        admin_user.hashed_password = pwd_context.hash(new_password)
        await admin_user.save()

        return RedirectResponse(url="/admin", status_code=HTTP_302_FOUND)