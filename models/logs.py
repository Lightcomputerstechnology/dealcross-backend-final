from tortoise import Model, fields

# ─────────── SYSTEM LOGS MODEL ───────────

class Logs(Model):
    id = fields.IntField(pk=True)
    message = fields.TextField()
    level = fields.CharField(max_length=50)  # Example: "INFO", "WARNING", "ERROR"
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.level}] {self.message[:30]}..."  # Show part of the log in admin/debug
