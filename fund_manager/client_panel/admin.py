from django.contrib import admin
from .models import Client, Investment

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'balance', 'created_at')

@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ('client', 'fund_index', 'amount_invested', 'shares_owned', 'created_at')
