from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Client, Investment
from admin_panel.models import FundIndex


def add_client(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")

        if Client.objects.filter(email=email).exists():
            messages.error(request, "A client with this email already exists.")
        else:
            Client.objects.create(name=name, email=email, phone=phone)
            messages.success(request, "Client added successfully!")
        return redirect('client_list')

    return render(request, 'client_panel/add_client.html')


def invest(request, client_id):
    client = Client.objects.get(pk=client_id)
    fund_indexes = FundIndex.objects.all()

    if request.method == "POST":
        fund_index_id = request.POST.get("fund_index")
        amount = float(request.POST.get("amount"))

        fund_index = FundIndex.objects.get(pk=fund_index_id)
        nav = fund_index.calculate_nav()  # Assume you have a method for NAV calculation

        shares = amount / nav  # Calculate the shares the client will own
        Investment.objects.create(client=client, fund_index=fund_index, amount_invested=amount, shares_owned=shares)
        value = float(client.balance)
        value += amount  # Update client's balance
        client.balance = value
        client.save()

        messages.success(request, f"Investment of ₹{amount} in {fund_index.name} successful!")
        return redirect('client_list')

    return render(request, 'client_panel/invest.html', {'client': client, 'fund_indexes': fund_indexes})


def client_list(request):
    clients = Client.objects.all()
    fund_indexes = FundIndex.objects.all()
    return render(request, 'client_panel/client_list.html', {'clients': clients, 'fund_indexes': fund_indexes})
