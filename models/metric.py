class Metric(Model):
    id = fields.IntField(pk=True)
    type = fields.CharField(max_length=100)
    value = fields.FloatField()
    timestamp = fields.DatetimeField(auto_now_add=True)
