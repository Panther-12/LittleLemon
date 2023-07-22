from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# Fields: id, name
class Category(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title
    
# Fields: name, price, description, category(ForeignKey)
class MenuItems(models.Model):
    name = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    inventory = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.name

class ItemOfTheDay(models.Model):
    title = models.ForeignKey(MenuItems, on_delete=models.PROTECT)

    def __str__(self):
        return self.title
    
# Fields: id, userid, status, items, amount
# Customer: api/orders, methods: POST
class CustomerOrders(models.Model):
    customer = models.ForeignKey(User, on_delete=models.PROTECT)
    items = models.TextField()
    amount = models.DecimalField(max_digits=6, decimal_places=2)


    def __str__(self):
        return self.items

# Delivery crew: api/orders
class AllocateOrders(models.Model):
    delivery_man = models.ForeignKey(User, on_delete=models.PROTECT)
    order = models.ForeignKey(CustomerOrders, on_delete=models.PROTECT)
    delivered = models.BooleanField(default=False)
    out_for_delivery = models.BooleanField(default=True)

    def __str__(self):
        return self.order

    def getStaffOrders(self, staffid):
        staff_orders = AllocateOrders.objects.filter(delivary_man=staffid)
        orders_array = []
        status = ""

        for order in staff_orders:
            if order.delivered:
                status = "delivered"
            if order.pending:
                status = "pending"
            orders_array.append(f"order_id:{order.order},status:{status}")
        return orders_array

# Fields: id, userid, item, price
# api/cart methods: get-Fetch customer cart, post-Add item to cart, delete-Delete item from cart
# The whole cart is deleted when an order is placeds
class CartItems(models.Model):
    customer = models.ForeignKey(User, on_delete=models.PROTECT)
    item = models.ForeignKey(MenuItems, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=1)

    def __int__(self):
        return self.item
    
    def generateCart(self, customerid):
        cart_items = CartItems.objects.filter(customer=customerid)
        if len(cart_items) <= 0:
            return "user cart is empty"
        cart_array = []
        print(cart_items)
        for item in cart_items:
            menu_item = MenuItems.objects.get(pk=item.item.pk)
            if menu_item:
                cart_array.append({"product":menu_item.name,"price":menu_item.price,"quantity":item.quantity})
        return cart_array

         



