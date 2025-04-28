class Share(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    price = fields.FloatField()
    change = fields.CharField(max_length=50, null=True)
