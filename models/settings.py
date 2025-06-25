from tortoise import fields, models

class AppSetting(models.Model):  # ✅ Clear, unambiguous name
    id = fields.IntField(pk=True)

    # Feature Toggles
    fees_enabled = fields.BooleanField(default=True)
    maintenance_mode = fields.BooleanField(default=False)
    registration_enabled = fields.BooleanField(default=True)

    # UI & Messaging
    announcement_text = fields.TextField(null=True)
    homepage_banner_url = fields.CharField(max_length=255, null=True)
    support_email = fields.CharField(max_length=255, null=True)
    terms_url = fields.CharField(max_length=255, null=True)

    # System Info
    updated_by = fields.CharField(max_length=100, null=True)
    version_tag = fields.CharField(max_length=20, default="v1.0")
    
    # Timestamps
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "system_settings"

    def __str__(self):
        return f"SystemSettings (v{self.version_tag})"