from django import forms
from .models import Stock, FundIndex



class StockForm(forms.ModelForm):
    fund_index = forms.ModelChoiceField(
        queryset=FundIndex.objects.all(),
        required=True,
        label="Fund Index",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Stock
        fields = ['symbol', 'name', 'price', 'quantity']  # Include fields for Stock only
        widgets = {
            'symbol': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter stock symbol (e.g., AAPL)'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter stock name (e.g., Apple Inc.)'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter initial stock price'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter quantity'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get('price')
        quantity = cleaned_data.get('quantity')

        if price is not None and price < 0:
            self.add_error('price', "Price cannot be negative.")

        if quantity is not None and quantity < 0:
            self.add_error('quantity', "Quantity cannot be negative.")

        return cleaned_data
