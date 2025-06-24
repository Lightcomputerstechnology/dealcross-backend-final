from tortoise import fields
from tortoise.models import Model

class BlogPost(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    slug = fields.CharField(max_length=255, unique=True)
    content = fields.TextField()
    published_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "blog_posts"
        ordering = ["-published_at"]

    def __str__(self):
        return f"{self.title} ({self.slug})"
