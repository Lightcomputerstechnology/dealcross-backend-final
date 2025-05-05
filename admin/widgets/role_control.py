# File: admin/widgets/role_control.py

from fastapi_admin.widgets import Widget
from starlette.requests import Request
from models.role import RolePermission
from tortoise.exceptions import DoesNotExist

class RolePermissionWidget(Widget):
    async def render(self, request: Request) -> str:
        roles = await RolePermission.all()
        role_forms = ""

        for role in roles:
            role_forms += f"""
            <form method="post" action="/admin/update-role/{role.id}" style="border:1px solid #ccc;padding:1rem;margin:1rem 0;">
                <h4>{role.role_name}</h4>
                <label><input type="checkbox" name="can_manage_users" {"checked" if role.can_manage_users else ""}> Manage Users</label><br>
                <label><input type="checkbox" name="can_manage_wallets" {"checked" if role.can_manage_wallets else ""}> Manage Wallets</label><br>
                <label><input type="checkbox" name="can_view_audit_logs" {"checked" if role.can_view_audit_logs else ""}> View Audit Logs</label><br>
                <label><input type="checkbox" name="can_update_settings" {"checked" if role.can_update_settings else ""}> Update Settings</label><br>
                <label><input type="checkbox" name="can_approve_kyc" {"checked" if role.can_approve_kyc else ""}> Approve KYC</label><br>
                <label><input type="checkbox" name="can_handle_disputes" {"checked" if role.can_handle_disputes else ""}> Handle Disputes</label><br><br>
                <button type="submit" style="padding:6px 14px;background:#28a745;color:white;border:none;border-radius:4px;">Save</button>
            </form>
            """

        return f"""
        <div style="background:#fff;padding:1.5rem;border-radius:10px;margin-top:2rem;box-shadow:0 0 8px #ccc;">
            <h3>Role-Based Permissions</h3>
            {role_forms}
        </div>
        """