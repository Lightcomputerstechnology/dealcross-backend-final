from tortoise import Model, fields

# ─────────── CONFIGURATION SETTINGS MODEL ───────────

class Config(Model):
    id = fields.IntField(pk=True)
    key = fields.CharField(max_length=100, unique=True)  # Slimmer, safer
    value = fields.TextField()  # Allow longer, flexible settings
    is_active = fields.BooleanField(default=True)

    def __str__(self):
        return f"Config(key='{self.key}', active={self.is_active})"
