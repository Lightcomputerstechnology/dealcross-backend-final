# File: models/investor_report.py

from tortoise import fields
from tortoise.models import Model

class InvestorReport(Model):
    id = fields.IntField(pk=True)
    user_id = fields.IntField()  # You can later change to ForeignKey if needed
    investment_summary = fields.TextField()
    total_deals = fields.IntField(default=0)
    active_deals = fields.IntField(default=0)
    completed_deals = fields.IntField(default=0)
    failed_deals = fields.IntField(default=0)
    earned_profit = fields.DecimalField(max_digits=18, decimal_places=2, default=0)
    loss_recorded = fields.DecimalField(max_digits=18, decimal_places=2, default=0)
    report_date = fields.DateField(auto_now_add=True)

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "investor_report"
        ordering = ["-report_date"]

    def __str__(self):
        return f"InvestorReport: User {self.user_id} on {self.report_date}"