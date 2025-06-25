from tortoise import Model, fields

# ─────────── SHARE MODEL ───────────

class Share(Model):  # ✅ Use Model (already imported correctly)
    id = fields.IntField(pk=True)
    company_name = fields.CharField(max_length=255)
    price = fields.DecimalField(max_digits=12, decimal_places=2)
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f"Share({self.company_name}: ${self.price})"

    class Meta:
        table = "share_assets"  # ✅ Explicit table name (plural, consistent)