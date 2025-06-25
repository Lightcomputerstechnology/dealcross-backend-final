from tortoise import fields, models

# ─────────── SYSTEM LOG ENTRY MODEL ───────────

class LogEntry(models.Model):  # ✅ Matches `from .logs import LogEntry`
    id = fields.IntField(pk=True)
    level = fields.CharField(max_length=20)  # e.g., INFO, WARNING, ERROR
    message = fields.TextField()
    source = fields.CharField(max_length=100, null=True)  # e.g., 'auth', 'payment'
    metadata = fields.JSONField(null=True)  # Optional structured data
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "log_entries"
        ordering = ["-created_at"]

    def __str__(self):
        return f"[{self.level}] {self.source or 'system'}: {self.message[:50]}..."