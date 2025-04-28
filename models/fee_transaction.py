class FeeTransaction(Model):
    id = fields.IntField(pk=True)
    amount = fields.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = fields.CharField(max_length=50)
    created_at = fields.DatetimeField(auto_now_add=True)
