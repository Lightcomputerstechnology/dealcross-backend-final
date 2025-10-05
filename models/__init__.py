# File: models/__init__.py
"""
Central model loader for Tortoise ORM.

⚙️ IMPORTANT:
Do NOT directly import one model inside another.
Instead, always reference other models as "models.<ModelName>" (string references).

Example:
    creator = fields.ForeignKeyField("models.User", related_name="deals")

This avoids circular import issues when Tortoise loads all models dynamically.
"""

from tortoise import Tortoise

# --- Import all model files explicitly for Tortoise to register ---
from .user import User
from .wallet import Wallet
from .wallet_transaction import WalletTransaction
from .admin_wallet import AdminWallet
from .admin_wallet_log import AdminWalletLog
from .kyc import KYCRequest
from .deal import Deal
from .dispute import Dispute
from .fraud import FraudAlert
from .audit import Audit
from .audit_log import AuditLog
from .metric import Metric
from .chart import ChartPoint
from .chat import ChatMessage
from .login_attempt import LoginAttempt
from .platform_earnings import PlatformEarnings
from .referral_reward import ReferralReward
from .support import SupportTicket
from .share import Share
from .settings import AppSetting
from .pending_approval import PendingApproval
from .banner import Banner
from .role_permission import RolePermission
from .webhook import WebhookLog
from .notification import Notification
from .investor_report import InvestorReport
from .escrow_tracker import EscrowTracker
from .fee_transaction import FeeTransaction
from .pairing import Pairing
from .blog import BlogPost
from .config import ConfigEntry
from .logs import LogEntry
from .aiinsight import AIInsightEntry
from .admin import Admin

__all__ = [
    "User",
    "Wallet",
    "WalletTransaction",
    "AdminWallet",
    "AdminWalletLog",
    "KYCRequest",
    "Deal",
    "Dispute",
    "FraudAlert",
    "Audit",
    "AuditLog",
    "Metric",
    "ChartPoint",
    "ChatMessage",
    "LoginAttempt",
    "PlatformEarnings",
    "ReferralReward",
    "SupportTicket",
    "Share",
    "AppSetting",
    "PendingApproval",
    "Banner",
    "RolePermission",
    "WebhookLog",
    "Notification",
    "InvestorReport",
    "EscrowTracker",
    "FeeTransaction",
    "Pairing",
    "BlogPost",
    "ConfigEntry",
    "LogEntry",
    "AIInsightEntry",
    "Admin",
]
