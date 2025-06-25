from tortoise import Model, fields

# ─────────── SHARE MODEL ───────────

class ShareAsset(Model):  # ✅ Renamed for clarity and consistency
    id = fields.IntField(pk=True)
    company_name = fields.CharField(max_length=255, null=False)
    price = fields.DecimalField(max_digits=12, decimal_places=2, null=False)
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f"ShareAsset({self.company_name}: ${self.price})"

    class Meta:
        table = "share_assets"  # ✅ Explicit DB table name for clarity