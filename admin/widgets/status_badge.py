from fastapi_admin.widgets import displays

class StatusBadge(displays.Display):
    async def render(self, request, value, **kwargs):
        color = {
            "open": "green",
            "pending": "yellow",
            "closed": "red"
        }.get(value, "gray")
        return f'<span class="px-2 py-1 rounded text-sm bg-{color}-200 text-{color}-800 font-medium">{value.title()}</span>'