# File: admin/widgets/summary_table.py

from fastapi_admin.widgets import Widget
from starlette.requests import Request
from tortoise.expressions import Q
from models.investor_report import InvestorReport
from jinja2 import Template

template_str = """
<div class="p-4 bg-white dark:bg-gray-800 rounded-xl shadow-md">
  <h2 class="text-lg font-bold text-gray-700 dark:text-white mb-2">Investor Summary</h2>
  <table class="min-w-full text-sm text-left text-gray-500 dark:text-gray-200">
    <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-200">
      <tr>
        <th class="py-2 px-4">Metric</th>
        <th class="py-2 px-4">Value</th>
      </tr>
    </thead>
    <tbody>
      <tr><td class="py-2 px-4">Total Reports</td><td class="py-2 px-4">{{ total }}</td></tr>
      <tr><td class="py-2 px-4">Total Deals</td><td class="py-2 px-4">{{ total_deals }}</td></tr>
      <tr><td class="py-2 px-4">Completed</td><td class="py-2 px-4">{{ completed }}</td></tr>
      <tr><td class="py-2 px-4">Failed</td><td class="py-2 px-4">{{ failed }}</td></tr>
      <tr><td class="py-2 px-4">Profit Earned</td><td class="py-2 px-4">${{ profit }}</td></tr>
      <tr><td class="py-2 px-4">Loss Recorded</td><td class="py-2 px-4">${{ loss }}</td></tr>
    </tbody>
  </table>
</div>
"""

class InvestorSummaryWidget(Widget):
    async def render(self, request: Request) -> str:
        reports = await InvestorReport.all()
        total = len(reports)
        total_deals = sum(r.total_deals for r in reports)
        completed = sum(r.completed_deals for r in reports)
        failed = sum(r.failed_deals for r in reports)
        profit = sum(r.earned_profit for r in reports)
        loss = sum(r.loss_recorded for r in reports)

        context = {
            "total": total,
            "total_deals": total_deals,
            "completed": completed,
            "failed": failed,
            "profit": profit,
            "loss": loss,
        }

        return Template(template_str).render(**context)