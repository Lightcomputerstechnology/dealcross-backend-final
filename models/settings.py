from tortoise import Model, fields

# ─────────── APP SETTINGS MODEL ───────────

class AppSettings(Model):
    id = fields.IntField(pk=True)
    setting_name = fields.CharField(max_length=255, unique=True, null=False)
    setting_value = fields.CharField(max_length=255, null=False)
    is_active = fields.BooleanField(default=True)

    # Optional: Human readable representation
    def __str__(self):
        return f"AppSettings({self.setting_name} = {self.setting_value}, active={self.is_active})"
