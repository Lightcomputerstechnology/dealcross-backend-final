class WalletTransaction(Model):
    id = fields.IntField(pk=True)
    wallet = fields.ForeignKeyField("models.Wallet", related_name="transactions", on_delete=fields.CASCADE)
    amount = fields.FloatField()
    transaction_type = fields.CharField(max_length=50)
    description = fields.CharField(max_length=255, null=True)
    timestamp = fields.DatetimeField(auto_now_add=True)
