class DealStatus(str, enum.Enum):
    pending = "pending"
    active = "active"
    completed = "completed"
    disputed = "disputed"
    cancelled = "cancelled"

class Deal(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    amount = fields.FloatField()
    status = fields.CharEnumField(DealStatus, default=DealStatus.pending)
    description = fields.CharField(max_length=255, null=True)
    public_deal = fields.BooleanField(default=False)
    is_flagged = fields.BooleanField(default=False)
    creator = fields.ForeignKeyField("models.User", related_name="created_deals", on_delete=fields.CASCADE)
    counterparty = fields.ForeignKeyField("models.User", related_name="counterparty_deals", on_delete=fields.CASCADE)
    fee_applied = fields.FloatField(default=0.0)
    created_at = fields.DatetimeField(auto_now_add=True)
