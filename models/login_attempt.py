from tortoise import Model, fields

# ─────────── LOGIN ATTEMPTS MODEL ───────────

class LoginAttempt(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="login_attempts", on_delete=fields.CASCADE)
    ip_address = fields.CharField(max_length=255)
    successful = fields.BooleanField()
    timestamp = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f"LoginAttempt(user_id={self.user_id}, ip={self.ip_address}, success={self.successful})"
