from fastapi.requests import Request
from fastapi_admin.widgets import Widget
from jinja2 import Template

class EscrowStatsWidget(Widget):
    async def render(self, request: Request) -> str:
        from models.escrow import EscrowTracker

        escrows = await EscrowTracker.all()
        total = len(escrows)
        active = sum(1 for e in escrows if e.status == "active")
        awaiting = sum(1 for e in escrows if e.status == "awaiting_release")
        completed = sum(1 for e in escrows if e.status == "released")
        overdue = sum(1 for e in escrows if e.status == "overdue")

        template = Template("""
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 p-4 bg-white dark:bg-gray-800 rounded-xl shadow-md mt-6">
          <div class="text-center">
            <p class="text-sm text-gray-500 dark:text-gray-300">Active</p>
            <h2 class="text-xl font-bold text-blue-600 dark:text-blue-400">{{ active }}</h2>
          </div>
          <div class="text-center">
            <p class="text-sm text-gray-500 dark:text-gray-300">Awaiting Release</p>
            <h2 class="text-xl font-bold text-yellow-600 dark:text-yellow-400">{{ awaiting }}</h2>
          </div>
          <div class="text-center">
            <p class="text-sm text-gray-500 dark:text-gray-300">Completed</p>
            <h2 class="text-xl font-bold text-green-600 dark:text-green-400">{{ completed }}</h2>
          </div>
          <div class="text-center">
            <p class="text-sm text-gray-500 dark:text-gray-300">Overdue</p>
            <h2 class="text-xl font-bold text-red-600 dark:text-red-400">{{ overdue }}</h2>
          </div>
        </div>
        """)

        return template.render(
            total=total,
            active=active,
            awaiting=awaiting,
            completed=completed,
            overdue=overdue,
        )