from tortoise import Model, fields

# ─────────── KYC REQUEST MODEL ───────────

class KYCRequest(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="kyc_requests", on_delete=fields.CASCADE)
    document_type = fields.CharField(max_length=255)
    document_url = fields.CharField(max_length=255)
    status = fields.CharField(max_length=50, default="pending")  # Shortened length, enough for 'pending', 'approved', 'rejected'
    submitted_at = fields.DatetimeField(auto_now_add=True)

    reviewed_by = fields.ForeignKeyField(
        "models.User",
        related_name="kyc_reviews",
        on_delete=fields.SET_NULL,  # Better: Don't delete KYC if reviewer is deleted
        null=True
    )
    review_note = fields.TextField(null=True)

    def __str__(self):
        return f"KYCRequest(user_id={self.user_id}, status={self.status})"
