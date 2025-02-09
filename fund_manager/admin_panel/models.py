from django.db import models
from django.utils.timezone import now


class Stock(models.Model):
    symbol = models.CharField(max_length=20, unique=True)  # e.g., AAPL
    name = models.CharField(max_length=100)  # e.g., Apple Inc.
    price = models.FloatField(default=0.0)  # Stock price
    quantity = models.FloatField(default=0.0)  # Quantity
    current_price = models.FloatField(default=0.0)  # Store the current price of the stock

    def __str__(self):
        return f"{self.symbol} - {self.name}"


class FundIndex(models.Model):
    name = models.CharField(max_length=50, unique=True)  # e.g., Tech Fund
    stocks = models.ManyToManyField(Stock, related_name='funds')  # Stocks in this fund
    created_at = models.DateTimeField(auto_now_add=True)

    total_units = models.FloatField(default=50000)  # Initial total units of the fund
    initial_nav = models.FloatField(default=10)  # Initial NAV

    def calculate_nav(self):
        """
        Calculate the Net Asset Value (NAV) of the FundIndex.
        NAV = Total Value of Stocks / Total Units
        """
        total_value = 0.0

        for stock in self.stocks.all():
            total_value += stock.current_price * stock.quantity

        if self.total_units > 0:
            
            print('@@@@@@@@@', total_value, self.total_units)
            nav = total_value / self.total_units
        else:
            nav = 0.0  # Avoid division by zero
        nav = round(nav, 2)
        NAVData.objects.update_or_create(
            fund_index=self,
            date=now().date(),  # Use today's date
            defaults={"value": nav}
        )

        return nav  # Return rounded NAV for simplicity

    def invest(self, amount_invested):
        """
        Add investment to the fund and calculate new units issued based on NAV.
        """
        current_nav = self.calculate_nav() or self.initial_nav  # If NAV is 0, use initial NAV
        new_units = amount_invested / current_nav
        self.total_units += new_units  # Increase the total units by the newly issued units
        self.save()
        self.calculate_nav()  # Recalculate NAV

    def __str__(self):
        return self.name


class NAVData(models.Model):
    fund_index = models.ForeignKey(FundIndex, on_delete=models.CASCADE, related_name='nav_data')
    date = models.DateField(default=now)
    value = models.FloatField()

    class Meta:
        unique_together = ('fund_index', 'date')  # Ensure one NAV entry per fund per day

    def __str__(self):
        return f"{self.fund_index.name} - {self.date}: {self.value}"


