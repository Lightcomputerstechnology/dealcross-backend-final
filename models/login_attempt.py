from tortoise import fields, models

class LoginAttempt(models.Model):
    id = fields.IntField(pk=True)

    user = fields.ForeignKeyField(
        "models.User",  # ✅ Correct format: app_label.ModelName
        related_name="login_attempts",
        on_delete=fields.CASCADE
    )

    ip_address = fields.CharField(max_length=255)
    user_agent = fields.CharField(max_length=255, null=True)  # Optional device info
    successful = fields.BooleanField()
    timestamp = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "login_attempts"
        ordering = ["-timestamp"]

    def __str__(self):
        status = "Success" if self.successful else "Failed"
        return f"LoginAttempt(user_id={self.user_id}, IP={self.ip_address}, {status})"