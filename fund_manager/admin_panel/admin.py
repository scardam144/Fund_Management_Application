from django.contrib import admin
from .models import FundIndex, Stock, NAVData

# Register your models here.


class StockAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'name', 'price', 'quantity')  # Show symbol, name, and price
    search_fields = ('symbol', 'name')  # Enable searching by symbol or name


class FundIndexAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')  # Show name and creation date
    filter_horizontal = ('stocks',)  # Allow easy management of stocks for the fund index
    search_fields = ('name',)  # Enable searching by fund name


class NAVDataAdmin(admin.ModelAdmin):
    list_display = ('fund_index', 'date', 'value')
    search_fields = ('fund_index__name', 'date')
    list_filter = ('date',)


# Register the models with the admin interface
admin.site.register(Stock, StockAdmin)
admin.site.register(FundIndex, FundIndexAdmin)
admin.site.register(NAVData, NAVDataAdmin)
