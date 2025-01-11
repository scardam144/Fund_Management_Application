from django.db import models
from admin_panel.models import FundIndex


class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Total fund the client holds
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def total_shares(self):
        total_shares = self.investments.aggregate(total_shares=models.Sum('shares_owned'))['total_shares'] or 0
        return total_shares


class Investment(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="investments")
    fund_index = models.ForeignKey(FundIndex, on_delete=models.CASCADE)
    amount_invested = models.DecimalField(max_digits=10, decimal_places=2)
    shares_owned = models.DecimalField(max_digits=10, decimal_places=4)  # NAV shares assigned
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client.name} - {self.fund_index.name}"