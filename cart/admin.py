from django.contrib import admin
from .models import Cart ,CartItem
# Register your models here.

# class CartAdmin(admin.ModelAdmin):
#     list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')
#     prepopulated_fields = {'slug': ('product_name',)}


admin.site.register(Cart)
admin.site.register(CartItem)
