from tortoise import Model, fields

# ─────────── SHARE MODEL ───────────

class Share(Model):
    id = fields.IntField(pk=True)
    company_name = fields.CharField(max_length=255, null=False)
    price = fields.DecimalField(max_digits=12, decimal_places=2, null=False)
    created_at = fields.DatetimeField(auto_now_add=True)

    # Optional: Human readable representation
    def __str__(self):
        return f"Share({self.company_name}: ${self.price})"
