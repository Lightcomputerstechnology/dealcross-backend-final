class Share(Model):
    id = fields.IntField(pk=True)
    company_name = fields.CharField(max_length=255)
    price = fields.DecimalField(max_digits=12, decimal_places=2)
    created_at = fields.DatetimeField(auto_now_add=True)
