class DisputeStatus(str, enum.Enum):
    open = "open"
    resolved = "resolved"
    rejected = "rejected"

class Dispute(Model):
    id = fields.IntField(pk=True)
    deal = fields.ForeignKeyField("models.Deal", related_name="disputes", on_delete=fields.CASCADE)
    user = fields.ForeignKeyField("models.User", related_name="disputes", on_delete=fields.CASCADE)
    reason = fields.CharField(max_length=255)
    details = fields.CharField(max_length=500, null=True)
    status = fields.CharEnumField(DisputeStatus, default=DisputeStatus.open)
    resolution_note = fields.CharField(max_length=500, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    resolved_at = fields.DatetimeField(null=True)
