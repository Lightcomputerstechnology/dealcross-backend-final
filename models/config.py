from tortoise import Model, fields

# ─────────── CONFIGURATION SETTINGS MODEL ───────────

class ConfigEntry(Model):  # ✅ Renamed to match your imports
    id = fields.IntField(pk=True)
    key = fields.CharField(max_length=100, unique=True)  # Slimmer, safer
    value = fields.TextField()  # Allow longer, flexible settings
    is_active = fields.BooleanField(default=True)

    def __str__(self):
        return f"ConfigEntry(key='{self.key}', active={self.is_active})"

    class Meta:
        table = "config_entries"