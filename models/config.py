from tortoise import Model, fields

# ─────────── SYSTEM LOG ENTRY MODEL ───────────

class LogEntry(Model):
    id = fields.IntField(pk=True)
    level = fields.CharField(max_length=50)  # e.g., INFO, WARNING, ERROR
    message = fields.TextField()
    origin = fields.CharField(max_length=100, null=True)  # e.g., "auth_module"
    metadata = fields.JSONField(null=True)  # Optional structured context
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f"LogEntry(level={self.level}, message={self.message[:30]}...)"

    class Meta:
        table = "log_entries"
        ordering = ["-created_at"]