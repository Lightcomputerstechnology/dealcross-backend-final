from fastapi_admin.resources import Model from fastapi_admin.widgets import inputs, displays, filters from fastapi_admin.depends import get_current_admin from tortoise import fields from typing import Optional

=====================

Role-Based Access Control

=====================

class SecureModel(Model): async def is_accessible(self, request): admin = await get_current_admin(request) return admin and getattr(admin, "is_superuser", False)

==========================

Core Admin Control Panels

==========================

class UserAdmin(SecureModel): label = "Users" model = "models.user.User" icon = "fa fa-user" search_fields = ["username", "email"] filters = [filters.Search(name="username"), filters.Boolean(name="is_superuser")] fields = [ "id", inputs.Text(name="username"), inputs.Email(name="email"), inputs.Boolean(name="is_superuser"), displays.Datetime(name="created_at") ]

class WalletAdmin(SecureModel): label = "Wallets" model = "models.wallet.Wallet"

class WalletTransactionAdmin(SecureModel): label = "Wallet Transactions" model = "models.wallet_transaction.WalletTransaction"

class KYCAdmin(SecureModel): label = "KYC" model = "models.kyc.KYC"

class DealAdmin(SecureModel): label = "Deals" model = "models.deal.Deal"

class DisputeAdmin(SecureModel): label = "Disputes" model = "models.dispute.Dispute"

class ReferralAdmin(SecureModel): label = "Referrals" model = "models.referral_reward.ReferralReward"

class EarningsAdmin(SecureModel): label = "Earnings" model = "models.platform_earnings.PlatformEarnings"

=============================

Monitoring and Visualization

=============================

class FraudAdmin(SecureModel): label = "Fraud Reports" model = "models.fraud.Fraud"

class AuditLogAdmin(SecureModel): label = "Audit Logs" model = "models.audit_log.AuditLog"

class AnalyticsOverview(SecureModel): label = "Analytics" model = "models.metric.Metric"

class MetricsChartAdmin(SecureModel): label = "Charts" model = "models.chart.Chart"

class NotificationLogAdmin(SecureModel): label = "Notifications" model = "models.notification.Notification"

class InvestorReportAdmin(SecureModel): label = "Investor Reports" model = "models.investor_report.InvestorReport"

class EscrowTrackerAdmin(SecureModel): label = "Escrow Tracker" model = "models.escrow.EscrowTracker"

=====================

Communication & Mods

=====================

class AdminChatThreadAdmin(SecureModel): label = "Deal Chats" model = "models.chat.Chat"

class SupportTicketAdmin(SecureModel): label = "Support Tickets" model = "models.support.SupportTicket"

==================

Share & Trading

==================

class ShareTradingAdmin(SecureModel): label = "Share Trading" model = "models.share.Share"

========================

Security & Configs

========================

class AdminLoginsAdmin(SecureModel): label = "Login Logs" model = "models.login_attempt.LoginAttempt"

class SystemSettingsAdmin(SecureModel): label = "System Settings" model = "models.settings.Settings"

class PendingApprovalAdmin(SecureModel): label = "Pending Approval" model = "models.pending_approval.PendingApproval"

==================

UI & Permissions

==================

class BannerManagerAdmin(SecureModel): label = "Banners" model = "models.banner.Banner"

class RolePermissionAdmin(SecureModel): label = "Permissions" model = "models.role.RolePermission"

class WebhookLogAdmin(SecureModel): label = "Webhooks" model = "models.webhook.WebhookLog"