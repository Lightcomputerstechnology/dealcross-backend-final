from tortoise import fields, models

# ─────────── AI INSIGHT ENTRY MODEL ───────────

class AIInsightEntry(models.Model):  # ✅ Matches import name
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    content = fields.TextField()
    source = fields.CharField(max_length=100, null=True)  # e.g., 'prediction', 'alert'
    tags = fields.JSONField(null=True)  # Optional list of tags or categories
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "ai_insight_entries"
        ordering = ["-created_at"]

    def __str__(self):
        return f"AIInsightEntry(title='{self.title}', source='{self.source}')"