from fastapi_admin.resources import Model
from fastapi_admin.widgets import inputs, displays, filters
from fastapi_admin.depends import get_current_admin
from tortoise import fields
from typing import Optional

# =====================
# Role-Based Access Control
# =====================

class SecureModel(Model):
    async def is_accessible(self, request):
        admin = await get_current_admin(request)
        return admin and getattr(admin, "is_superuser", False)

# ==========================
# Core Admin Control Panels
# ==========================

class UserAdmin(SecureModel):
    label = "Users"
    model = "models.User"
    icon = "fa fa-user"
    search_fields = ["username", "email"]
    filters = [filters.Search(name="username"), filters.Boolean(name="is_superuser")]
    fields = [
        "id",
        inputs.Text(name="username"),
        inputs.Email(name="email"),
        inputs.Boolean(name="is_superuser"),
        displays.Datetime(name="created_at")
    ]

class WalletAdmin(SecureModel):
    label = "Wallets"
    model = "models.Wallet"

class WalletTransactionAdmin(SecureModel):
    label = "Wallet Transactions"
    model = "models.WalletTransaction"

class KYCAdmin(SecureModel):
    label = "KYC"
    model = "models.KYC"

class DealAdmin(SecureModel):
    label = "Deals"
    model = "models.Deal"

class DisputeAdmin(SecureModel):
    label = "Disputes"
    model = "models.Dispute"

class ReferralAdmin(SecureModel):
    label = "Referrals"
    model = "models.ReferralReward"

class EarningsAdmin(SecureModel):
    label = "Earnings"
    model = "models.PlatformEarning"

# =============================
# Monitoring and Visualization
# =============================

class FraudAdmin(SecureModel):
    label = "Fraud Reports"
    model = "models.FraudAlert"

class AuditLogAdmin(SecureModel):
    label = "Audit Logs"
    model = "models.AuditLog"

class AnalyticsOverview(SecureModel):
    label = "Analytics"
    model = "models.Metric"

class MetricsChartAdmin(SecureModel):
    label = "Charts"
    model = "models.Chart"

class NotificationLogAdmin(SecureModel):
    label = "Notifications"
    model = "models.Notification"

class InvestorReportAdmin(SecureModel):
    label = "Investor Reports"
    model = "models.InvestorReport"

class EscrowTrackerAdmin(SecureModel):
    label = "Escrow Tracker"
    model = "models.EscrowTracker"

# =====================
# Communication & Mods
# =====================

class AdminChatThreadAdmin(SecureModel):
    label = "Deal Chats"
    model = "models.ChatMessage"

class SupportTicketAdmin(SecureModel):
    label = "Support Tickets"
    model = "models.SupportTicket"

# ==================
# Share & Trading
# ==================

class ShareTradingAdmin(SecureModel):
    label = "Share Trading"
    model = "models.Share"

# ========================
# Security & Configs
# ========================

class AdminLoginsAdmin(SecureModel):
    label = "Login Logs"
    model = "models.LoginAttempt"

class SystemSettingsAdmin(SecureModel):
    label = "System Settings"
    model = "models.Settings"

class PendingApprovalAdmin(SecureModel):
    label = "Pending Approval"
    model = "models.PendingApproval"

# ==================
# UI & Permissions
# ==================

class BannerManagerAdmin(SecureModel):
    label = "Banners"
    model = "models.Banner"

class RolePermissionAdmin(SecureModel):
    label = "Permissions"
    model = "models.RolePermission"

class WebhookLogAdmin(SecureModel):
    label = "Webhooks"
    model = "models.WebhookLog"