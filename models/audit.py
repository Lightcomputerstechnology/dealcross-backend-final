class Audit(Model):
    id = fields.IntField(pk=True)
    action = fields.CharField(max_length=255)
    performed_by = fields.ForeignKeyField("models.User", related_name="audits", on_delete=fields.CASCADE)
    created_at = fields.DatetimeField(auto_now_add=True)
