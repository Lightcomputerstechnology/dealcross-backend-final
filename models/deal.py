class Deal(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="deals", on_delete=fields.CASCADE)
    status = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)
