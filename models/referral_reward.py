# models/referral_reward.py
from tortoise import fields, models

class ReferralReward(models.Model):
    id = fields.IntField(pk=True)
    referrer = fields.ForeignKeyField("models.User", related_name="rewards")
    referred = fields.ForeignKeyField("models.User", related_name="earned_rewards")
    source = fields.CharField(max_length=50)  # "wallet" or "deal"
    amount = fields.DecimalField(max_digits=12, decimal_places=2)
    timestamp = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "referral_rewards"
        unique_together = ("referred", "source")  # Prevent multiple rewards per action
