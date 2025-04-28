class EscrowTracker(Model):
    id = fields.IntField(pk=True)
    deal = fields.ForeignKeyField("models.Deal", related_name="escrow_trackers", on_delete=fields.CASCADE)
    status = fields.CharField(max_length=50, default="initiated")
    amount_held = fields.FloatField()
    last_updated = fields.DatetimeField(auto_now=True)
