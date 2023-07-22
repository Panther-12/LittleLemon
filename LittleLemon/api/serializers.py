from .models import Category, MenuItems, CartItems, AllocateOrders, CustomerOrders, ItemOfTheDay
from django.contrib.auth.models import User
from restaurant.models import Booking
from rest_framework import serializers



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UserGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','title','description']


# Menu items relationship serializer
class MenuItemSerializer(serializers.ModelSerializer):
    # price_after_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = MenuItems
        fields = ['id','name','price','description','inventory','category','category_id']
        extra_kwargs = {
            'price': {'min_value': 0}
        }

    # def calculate_tax(self, item:MenuItems):
    #     return item.price * 0.05

class CartSerializer(serializers.ModelSerializer):
    customer = UserSerializer(read_only=True)
    item = MenuItemSerializer(read_only=True)

    customer_id = serializers.IntegerField(write_only=True)
    item_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = CartItems
        fields = ['id','customer', 'item', 'quantity', 'customer_id','item_id']

class CustomerOrderSerializer(serializers.ModelSerializer):
    customer = UserSerializer(read_only=True)
    customer_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = CustomerOrders
        fields = ['id', 'customer', 'customer_id', 'items', 'amount']

class CreateOrderSerializer(serializers.ModelSerializer):
    customer = UserSerializer(read_only=True)
    class Meta:
        model = CustomerOrders
        fields = ['id', 'customer']

class ListOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllocateOrders
        fields = '__all__'

class AllocateOrdersSerializer(serializers.ModelSerializer):
    delivery_man = UserSerializer(read_only=True)
    delivery_man_id = serializers.IntegerField(write_only=True)
    order = CustomerOrderSerializer(read_only=True)
    order_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = AllocateOrders
        fields = ['delivery_man','delivery_man_id','order','order_id']

class UpdateOrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllocateOrders
        fields = ['delivered','out_for_delivery']

class UpdateItemOfTheDaySerializer(serializers.ModelSerializer):
    title = MenuItemSerializer(read_only=True)
    title_id = MenuItemSerializer(write_only=True)
    class Meta:
        model = ItemOfTheDay
        fields = ['id','title','title_id']

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
