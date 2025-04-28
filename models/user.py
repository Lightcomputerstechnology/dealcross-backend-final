from tortoise import fields
from tortoise.models import Model
import enum

class UserRole(str, enum.Enum):
    user = "user"
    moderator = "moderator"
    auditor = "auditor"
    admin = "admin"

class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=255, unique=True)
    email = fields.CharField(max_length=255, unique=True)
    hashed_password = fields.CharField(max_length=255)
    role = fields.CharEnumField(UserRole, default=UserRole.user)

    # Relationships
    kyc_requests = fields.ReverseRelation["KYCRequest"]
    reviewed_kyc_requests = fields.ReverseRelation["KYCRequest"]
    created_deals = fields.ReverseRelation["Deal"]
    counterparty_deals = fields.ReverseRelation["Deal"]
    disputes = fields.ReverseRelation["Dispute"]
    reported_fraud_alerts = fields.ReverseRelation["FraudAlert"]
    audit_logs = fields.ReverseRelation["AuditLog"]
    wallet = fields.ReverseRelation["Wallet"]
