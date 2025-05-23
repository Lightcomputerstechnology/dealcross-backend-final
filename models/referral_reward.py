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
        max_length=30  # E.g., "wallet_funding", "deal_funding"
    )

    amount = fields.DecimalField(
        max_digits=12, decimal_places=2
    )

    approved_by_admin = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "referral_rewards"
        ordering = ["-created_at"]
        unique_together = ("referred", "source")

    def __str__(self):
        return (
            f"Reward {self.amount} from {self.referrer_id} for {self.referred_id} ({self.source})"
        )