class FraudAlert(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="fraud_alerts", on_delete=fields.CASCADE)
    alert_type = fields.CharField(max_length=255)
    description = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
