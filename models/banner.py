# File: models/banner.py

from tortoise import fields, models
from tortoise.models import Model
from enum import Enum


class BannerPosition(str, Enum):
    HERO = "hero"
    SIDEBAR = "sidebar"
    FOOTER = "footer"
    POPUP = "popup"


class Banner(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=100)
    image_url = fields.CharField(max_length=300)
    link = fields.CharField(max_length=300, null=True)
    position = fields.CharEnumField(BannerPosition, default=BannerPosition.HERO)
    is_active = fields.BooleanField(default=True)
    expiration_date = fields.DatetimeField(null=True)
    clicks = fields.IntField(default=0)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "banner"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.position})"