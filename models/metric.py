class Metric(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    value = fields.FloatField()
    timestamp = fields.DatetimeField(auto_now_add=True)
