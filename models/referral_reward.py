# File: models/referral_reward.py

from tortoise import fields, models

class ReferralReward(models.Model):
    id = fields.IntField(pk=True)
    referrer = fields.ForeignKeyField("models.User", related_name="referral_earnings")
    referred = fields.ForeignKeyField("models.User", related_name="referral_rewards")
    source = fields.CharField(max_length=20)  # "wallet" or "deal"
    amount = fields.DecimalField(max_digits=12, decimal_places=2)
    timestamp = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "referral_rewards"
        unique_together = ("referred", "source")  # One reward per source per user

    def __str__(self):
        return f"ReferralReward(from={self.referred_id}, to={self.referrer_id}, source={self.source}, amount={self.amount})"
