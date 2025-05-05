from fastapi_admin.widgets import displays

class ImageDisplay(displays.Display):
    async def render(self, request, value, **kwargs):
        return f'<img src="{value}" alt="Banner" style="max-height: 60px; border-radius: 6px;" />'