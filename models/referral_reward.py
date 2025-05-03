# File: models/referral_reward.py

from tortoise import fields, models

class ReferralReward(models.Model):
    id = fields.IntField(pk=True)
    
    referrer = fields.ForeignKeyField(
        "models.User",
        related_name="referral_earnings",
        on_delete=fields.CASCADE
    )
    referred = fields.ForeignKeyField(
        "models.User",
        related_name="referral_rewards",
        on_delete=fields.CASCADE
    )
    
    source = fields.CharField(
        max_length=30
    )  # E.g., "wallet_funding", "deal_funding"
    
    amount = fields.DecimalField(
        max_digits=12, decimal_places=2
    )
    
    approved_by_admin = fields.BooleanField(default=False)  # ✅ NEW for manual control
    
    timestamp = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "referral_rewards"
        unique_together = ("referred", "source")  # Only 1 reward per source per referred user

    def __str__(self):
        return (
            f"ReferralReward(from={self.referred_id}, to={self.referrer_id}, "
            f"source={self.source}, amount={self.amount})"
        )