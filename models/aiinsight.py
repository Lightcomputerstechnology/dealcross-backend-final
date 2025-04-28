from tortoise import Model, fields

# ─────────── AI INSIGHTS MODEL ───────────

class AIInsight(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    description = fields.TextField()
    confidence = fields.FloatField()
    created_at = fields.DatetimeField(auto_now_add=True)  # ✅ Added timestamp for better tracking

    def __str__(self):
        return f"AIInsight(id={self.id}, title='{self.title[:20]}...')"
