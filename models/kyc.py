class KYCRequest(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="kyc_requests", on_delete=fields.CASCADE)
    document_type = fields.CharField(max_length=255)
    document_url = fields.CharField(max_length=255)
    status = fields.CharField(max_length=255, default="pending")
    submitted_at = fields.DatetimeField(auto_now_add=True)
    reviewed_by = fields.ForeignKeyField("models.User", related_name="kyc_reviews", on_delete=fields.CASCADE, null=True)
    review_note = fields.TextField(null=True)
