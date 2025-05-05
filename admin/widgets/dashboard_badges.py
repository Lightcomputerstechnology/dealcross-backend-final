# File: admin/widgets/dashboard_badges.py

from fastapi_admin.widgets import Widget
from starlette.requests import Request
from tortoise.expressions import Q

from models.pending_approval import PendingApproval
from models.support import SupportTicket
from models.kyc import KYC
from models.deal import Deal
from models.login_attempt import LoginAttempt


class MetricBadge(Widget):
    def __init__(self, label: str, count: int, color: str):
        self.label = label
        self.count = count
        self.color = color

    async def render(self, request: Request) -> str:
        return f"""
        <div style='background:#fff; padding:1rem; border-radius:8px; text-align:center; box-shadow:0 0 6px #ccc; min-width:180px;'>
            <h4 style='margin:0; font-size:1rem;'>{self.label}</h4>
            <p style='font-size:2rem; font-weight:bold; color:{self.color}; margin: 0.5rem 0;'>{self.count}</p>
        </div>
        """


class DashboardBadgeGroup(Widget):
    async def render(self, request: Request) -> str:
        pending_kyc = await KYC.filter(status="pending").count()
        pending_deals = await Deal.filter(status="pending").count()
        pending_approvals = await PendingApproval.filter(status="pending").count()
        support_tickets = await SupportTicket.filter(status="open").count()
        failed_logins = await LoginAttempt.filter(success=False).count()

        badges = [
            MetricBadge("Pending KYC", pending_kyc, "#007bff"),
            MetricBadge("Pending Deals", pending_deals, "#6f42c1"),
            MetricBadge("Pending Approvals", pending_approvals, "#ff8800"),
            MetricBadge("Open Support Tickets", support_tickets, "#dc3545"),
            MetricBadge("Failed Logins", failed_logins, "#17a2b8"),
        ]

        rendered = await asyncio.gather(*(badge.render(request) for badge in badges))
        return "<div style='display:flex; flex-wrap:wrap; gap:1rem;'>" + "".join(rendered) + "</div>"