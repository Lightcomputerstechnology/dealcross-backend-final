class AuditLog(Model):
    id = fields.IntField(pk=True)
    action = fields.CharField(max_length=255)
    performed_by = fields.ForeignKeyField("models.User", related_name="audit_logs", on_delete=fields.CASCADE)
    timestamp = fields.DatetimeField(auto_now_add=True)
