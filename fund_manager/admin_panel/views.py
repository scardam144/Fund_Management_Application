from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import FundIndex, Stock, NAVData
from .utils import get_stock_price  # Import the utility function to fetch stock price
from .forms import StockForm
from django.contrib import messages
from datetime import date


@login_required
def dashboard(request):
    # Fetch all fund indexes from the database
    fund_indexes = FundIndex.objects.all()

    # Create a list to store the stock and price details
    stocks_data = []
    nav_data = {
        "dates": [],
        "values": [],
    }

    for fund in fund_indexes:
        # Ensure the initial NAV for 2025-01-01 is present
        initial_date = date(2025, 1, 1)
        initial_nav_entry, created = NAVData.objects.get_or_create(
            fund_index=fund,
            date=initial_date,
            defaults={"value": 10.0}
        )

        # Recalculate and save the current NAV for the fund
        current_nav = fund.calculate_nav()
        print(f"{current_nav}")

        # Fetch historical NAV data for the fund
        historical_navs = NAVData.objects.filter(fund_index=fund).order_by('date')

        # Populate nav_data for the chart
        nav_data["dates"] = [nav.date.strftime("%Y-%m-%d") for nav in historical_navs]
        nav_data["values"] = [nav.value for nav in historical_navs]

        # Process stock details for each fund
        for stock in fund.stocks.all():
            # Fetch the latest stock price using the utility function
            if stock.name == 'OTHER': #wjke
                stock.current_price = 2550
            else:
                stock.current_price = get_stock_price(stock.symbol)

            # Calculate values for each stock
            try:
                investment_value = stock.price * stock.quantity
                current_value = float(stock.current_price) * stock.quantity
                profit_loss = current_value - investment_value
            except:
                pass

            # Add the stock details to stocks_data
            stocks_data.append({
                'name': stock.name,
                'stock_price': stock.price,
                'quantity': stock.quantity,
                'investment_value': round(investment_value, 2),
                'current_price': round(stock.current_price, 2),
                'current_value': round(current_value, 2),
                'profit_loss': round(profit_loss, 2),
            })
            
            stock.save()

    # Calculate total investment value and current investment value
    total_investment_value = sum(data['investment_value'] for data in stocks_data)
    total_current_value = sum(data['current_value'] for data in stocks_data)
    total_profit_loss = total_current_value - total_investment_value
    print(f"{nav_data}")
    # nav_data = {
    #     "dates": ["2025-01-01", "2025-01-02", "2025-01-03"],  # Example dates
    #     "values": [10, 12, 15],  # Example NAV values
    # }
    stocks_data = sorted(stocks_data, key=lambda x: x['name'])
    print(f"{type(nav_data)}, {nav_data}")
    return render(request, 'admin_panel/dashboard.html', {
        'fund_indexes': fund_indexes,
        'stocks_data': stocks_data,
        'total_investment_value': round(total_investment_value, 2),
        'total_current_value': round(total_current_value, 2),
        'total_profit_loss': round(total_profit_loss, 2),
        "nav_data": nav_data,
    })


def add_stock(request):
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            stock = form.save()  # Save the stock
            fund_index = form.cleaned_data['fund_index']  # Get the selected FundIndex
            fund_index.stocks.add(stock)  # Associate the stock with the FundIndex
            fund_index.save()
            messages.success(request, f"Stock '{stock.symbol}' added to fund '{fund_index.name}'!")
            return redirect('dashboard')  # Redirect to the dashboard
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = StockForm()

    stocks = Stock.objects.all()
    return render(request, 'admin_panel/add_stock.html', {'form': form, 'stocks': stocks})

