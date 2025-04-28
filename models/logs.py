class Logs(Model):
    id = fields.IntField(pk=True)
    message = fields.TextField()
    level = fields.CharField(max_length=50)
    created_at = fields.DatetimeField(auto_now_add=True)
