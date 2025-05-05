from tortoise import fields, models

class Banner(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=100)
    image_url = fields.CharField(max_length=300)
    link = fields.CharField(max_length=300, null=True)
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "banner"

    def __str__(self):
        return self.title