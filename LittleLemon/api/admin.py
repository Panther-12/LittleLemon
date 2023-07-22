from django.contrib import admin
from .models import MenuItems, Category, CartItems, AllocateOrders

# Register your models here.
admin.site.register(MenuItems)
admin.site.register(Category)
admin.site.register(AllocateOrders)
admin.site.register(CartItems)