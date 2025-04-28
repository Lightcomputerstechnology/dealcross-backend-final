class AppSettings(Model):
    id = fields.IntField(pk=True)
    setting_name = fields.CharField(max_length=255, unique=True)
    setting_value = fields.CharField(max_length=255)
    is_active = fields.BooleanField(default=True)
