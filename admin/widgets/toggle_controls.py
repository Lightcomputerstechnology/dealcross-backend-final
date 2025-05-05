# File: admin/widgets/toggle_controls.py

from fastapi_admin.widgets import Widget
from starlette.requests import Request
from models.settings import Settings

class ToggleControlWidget(Widget):
    async def render(self, request: Request) -> str:
        # Get or create default settings
        settings = await Settings.first()
        if not settings:
            settings = await Settings.create(fees_enabled=True, maintenance_mode=False)

        return f"""
        <div style="background:#fff;padding:1.2rem;margin-top:2rem;border-radius:8px;box-shadow:0 0 6px #ccc;">
            <h4>System Toggle Controls</h4>
            <form method="post" action="/admin/toggle-settings" style="margin-top:1rem;">
                <label>
                    <input type="checkbox" name="fees_enabled" {"checked" if settings.fees_enabled else ""}>
                    Enable Platform Fees
                </label><br><br>
                <label>
                    <input type="checkbox" name="maintenance_mode" {"checked" if settings.maintenance_mode else ""}>
                    Maintenance Mode
                </label><br><br>
                <button type="submit" style="padding:8px 20px;background:#007bff;color:#fff;border:none;border-radius:4px;">
                    Save Settings
                </button>
            </form>
        </div>
        """