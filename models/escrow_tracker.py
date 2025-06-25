from tortoise import Model, fields

class EscrowTracker(Model):
    id = fields.IntField(pk=True)

    deal = fields.ForeignKeyField(
        "models.Deal",  # ✅ Correct format: "app_label.ModelName"
        related_name="escrow_trackers",
        on_delete=fields.CASCADE
    )

    amount = fields.DecimalField(max_digits=12, decimal_places=2)
    status = fields.CharField(max_length=50, default="pending")
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "escrow_trackers"

    def __str__(self):
        return f"EscrowTracker(deal_id={self.deal_id}, status={self.status}, amount={self.amount})"