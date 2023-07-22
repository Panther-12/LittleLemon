from django.shortcuts import render, get_object_or_404
from .serializers import CategorySerializer, MenuItemSerializer, CartSerializer, UserGroupSerializer, BookingSerializer
from .serializers import CustomerOrderSerializer, AllocateOrdersSerializer, CreateOrderSerializer, UpdateOrderStatusSerializer,ListOrdersSerializer, UserSerializer, UpdateItemOfTheDaySerializer
from rest_framework.decorators import api_view, throttle_classes, permission_classes
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User,Group
from restaurant.models import Booking
from .models import MenuItems, Category, CartItems, CustomerOrders, AllocateOrders
from .throttles import TenCallsPerMin
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
# import json
# from requests import post, get
# from django.http import HttpResponse
from .decorators import manager_required, delivery_crew_required
from .utils import calculate_total_cost, filter_data, paginate_items, order_by_category


# Create your views here.
# Function based views
@api_view(['GET','POST'])
@throttle_classes([AnonRateThrottle])
def menu_items(request):
    if request.method == 'GET':
        items = MenuItems.objects.select_related('category').all()
        items = filter_data(request,items)
        items = order_by_category(items)
        items = paginate_items(request, items)
        serialized_item = MenuItemSerializer(items, many=True)
        return Response(serialized_item.data, status.HTTP_200_OK)
    
    if request.method == 'POST':
        if request.user.groups.filter(name="Manager"):
            serialized_data = MenuItemSerializer(data=request.data)
            if serialized_data.is_valid():
                serialized_data.save()
                return Response(serialized_data.data, status.HTTP_201_CREATED)
        return Response({"message":"only managers allower"},status.HTTP_405_METHOD_NOT_ALLOWED)
    return Response(status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT','DELETE'])
@throttle_classes([AnonRateThrottle])
def single_item(request, menuItem):
    try:
        menu_item = MenuItems.objects.get(pk=menuItem)
    except menu_item.DoesNotExist:
        return Response(status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serialized_item = MenuItemSerializer(menu_item)
        return Response(serialized_item.data, status.HTTP_200_OK)
    
    if request.user.groups.filter(name="Manager"):
        if request.method == 'PUT':
            serialized_item = MenuItemSerializer(menu_item, data=request.data)
            if serialized_item.is_valid():
                serialized_item.save()
                return Response(serialized_item.data, status.HTTP_200_OK)
        if request.method == 'DELETE':
            menu_item.delete()
            return Response(status.HTTP_200_OK)
    else:
        return Response(status.HTTP_403_FORBIDDEN)
    return Response(status.HTTP_400_BAD_REQUEST)


@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
@manager_required
def category(request):
    admins = ['manager13@gmail.com']
    if request.method == 'GET':
        items = Category.objects.all()
        serialized_item = CategorySerializer(items, many=True) # "many=True" is required when getting multiple items
        return Response(serialized_item.data, status.HTTP_200_OK)
    if request.user.groups.filter(name="Manager") and request.user.email in admins:
        if request.method == 'POST':
            deserialized_item = CategorySerializer(data=request.data)
            deserialized_item.is_valid(raise_exception=True)
            deserialized_item.save()
            return Response(deserialized_item.validated_data, status.HTTP_201_CREATED)
    return Response(status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def orders(request):
    user = User.objects.filter(username=request.user)[0].id
    if request.method == "GET":
        if request.user.groups.filter(name="Manager"):
            products = CustomerOrders.objects.all()
            products = filter_data(request, products)
            products = paginate_items(request, products)
            serialized_product = CustomerOrderSerializer(products, many=True)
            return Response(serialized_product.data, status.HTTP_200_OK)
        
        if request.user.groups.filter(name="Delivery crew"):
            orders = AllocateOrders.objects.filter(delivery_man=user)
            orders = filter_data(request,orders)
            orders = paginate_items(orders)
            serialized_orders = ListOrdersSerializer(orders, many=True)
            return Response(serialized_orders.data, status.HTTP_200_OK)
        
        customer_products = CustomerOrders.objects.filter(customer=user)
        customer_products = filter_data(customer_products)
        customer_products = paginate_items(customer_products)
        if len(customer_products)>0:
            serialized_product = CustomerOrderSerializer(customer_products, many=True)
            return Response(serialized_product.data, status.HTTP_200_OK)
        return Response({"message":"no orders made by the user"}, status.HTTP_204_NO_CONTENT)
        
    if request.method == 'POST':
        if request.user.groups.filter(name="Manager") or request.user.groups.filter(name="Delivery crew"):
            return Response("Only customers can post orders", status.HTTP_403_FORBIDDEN)
        

        customer_cart = CartItems()
        order_cart = customer_cart.generateCart(customerid=user)

        customer_id = user
        items = [x['product'] for x in order_cart]
        amount = calculate_total_cost(order_cart)
        json_data = {"customer_id": customer_id, "items": str(items), "amount": str(amount)}

        new_serialized_order = CustomerOrderSerializer(data=json_data)
        if new_serialized_order.is_valid(raise_exception=True):
            new_serialized_order.save()

            clear_cart = CartItems.objects.filter(customer=user)
            for item in clear_cart:
                item.delete()
            return Response(new_serialized_order.data, status.HTTP_201_CREATED)
    return Response(status.HTTP_400_BAD_REQUEST)

@api_view(['PUT','DELETE','GET','PATCH'])
@permission_classes([IsAuthenticated])
def single_order(request, orderId):
    user = User.objects.filter(username=request.user)[0].id
    try:
        order = CustomerOrders.objects.get(pk=orderId)
    except order.DoesNotExist:
        return Response({"message":"order not found"}, status.HTTP_204_NO_CONTENT)
    
    if len(request.user.groups.filter(name="Manager"))<=0 and len(request.user.groups.filter(name="Delivery crew"))<=0:
        if order.customer == request.user:
            if request.method == 'GET':
                serialized_order = CustomerOrderSerializer(order)
                return Response(serialized_order.data, status.HTTP_200_OK)
            if request.method == 'PUT':
                serialized_order = CustomerOrderSerializer(order, data=request.data)
                if serialized_order.is_valid():
                    serialized_order.save()
                    return Response(serialized_order.validated_data, status.HTTP_200_OK)
            return Response(status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Order item does not belong to you"}, status.HTTP_401_UNAUTHORIZED)
    
    if request.user.groups.filter(name="Manager"):
        if request.method == 'GET':
            serialized_order = CustomerOrderSerializer(order)
            return Response(serialized_order.data, status.HTTP_200_OK)
        if request.method == 'PUT':
            order = AllocateOrders.objects.filter(order=orderId)
            serialized_data = AllocateOrdersSerializer(data=request.data)
            if serialized_data.is_valid(raise_exception=True):
                if len(order)>0:
                    return Response({"message": "Order already assigned"}, status.HTTP_200_OK)
                order_id = serialized_data.validated_data.get('order_id')
                print(order_id)
                if order_id == orderId:
                    serialized_data.save()
                    return Response(serialized_data.validated_data, status.HTTP_201_CREATED)
                return Response({"message": "Order id does not match the current id"}, status.HTTP_400_BAD_REQUEST)
        if request.method == 'PATCH':
            serialized_data = UpdateOrderStatusSerializer(data=request.data)
            if serialized_data.is_valid(raise_exception=True):
                delivered = serialized_data.data.get('delivered')
                out_for_delivery = serialized_data.data.get('out_for_delivery')

                order = AllocateOrders.objects.filter(order=orderId)
                if len(order)>0:
                    update_order = order[0]
                    update_order.delivered = delivered
                    update_order.out_for_delivery = out_for_delivery
                    update_order.save(update_fields=['delivered','out_for_delivery'])
                    return Response(ListOrdersSerializer(update_order).data, status.HTTP_200_OK)
                return Response(status.HTTP_204_NO_CONTENT)
        if request.method == 'DELETE':
            order.delete()
            return Response({"message": "Order deleted successfully"}, status.HTTP_200_OK)
        return Response(status.HTTP_400_BAD_REQUEST)
        
    if request.user.groups.filter(name="Delivery crew"):
        try:
            order = AllocateOrders.objects.filter(order=orderId)
        except order.DoesNotExist:
            return Response(status.HTTP_404_NOT_FOUND)
        if request.method == 'GET':
            serialized_order = AllocateOrdersSerializer(order[0])
            return Response(serialized_order.data, status.HTTP_200_OK)
        if request.method == 'PUT' or request.method=='PATCH':
            serialized_data = UpdateOrderStatusSerializer(data=request.data)
            if serialized_data.is_valid(raise_exception=True):
                delivered = serialized_data.data.get('delivered')
                out_for_delivery = serialized_data.data.get('out_for_delivery')
                if len(order)>0:
                    update_order = order[0]
                    update_order.delivered = delivered
                    update_order.out_for_delivery = out_for_delivery
                    update_order.save(update_fields=['delivered','out_for_delivery'])
                    return Response(ListOrdersSerializer(update_order).data, status.HTTP_200_OK)
                return Response(status.HTTP_204_NO_CONTENT)
        return Response(status.HTTP_400_BAD_REQUEST)



        

@api_view(['GET','POST','DELETE'])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def cart(request):
    if request.user.groups.filter(name="Manager") or request.user.groups.filter(name="Delivery crew"):
        return Response({"message": "Only customers can add items to cart"}, status.HTTP_403_FORBIDDEN)
    
    current_user = User.objects.filter(username=request.user)[0].id
    if request.method == "POST": # Customer id is automatically filled from the request.user object
        serialized_data = CartSerializer(data=request.data)
        if serialized_data.is_valid(raise_exception=True):
            serialized_data.save()
            return Response(serialized_data.data, status.HTTP_201_CREATED)
    if request.method == "GET":
        if len(CartItems.objects.filter(customer=current_user)) <= 0:
            return Response({"message": "No item in the cart"}, status.HTTP_204_NO_CONTENT)
        cart = CartItems()
        user_cart =cart.generateCart(customerid=current_user)
        total = calculate_total_cost(user_cart)
        return Response({"Cart": user_cart, "Total":total}, status.HTTP_200_OK)
    if request.method == 'DELETE':
        user_cart = CartItems.objects.filter(customer=current_user)
        for item in user_cart:
            item.delete()
        return Response({"message": "Cart deleted"}, status.HTTP_200_OK)
    return Response({}, status.HTTP_200_OK)


@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
@manager_required
def managers(request):
    if request.method == 'GET':
        manager_list = User.objects.filter(groups__name="Manager")
        serialized_data = UserSerializer(manager_list, many=True)
        return Response(serialized_data.data, status.HTTP_200_OK)
    if request.method == 'POST':
        serialized_data = UserGroupSerializer(data=request.data)
        user = User.objects.get(username=serialized_data.data.get('username'))
        group = Group.objects.get(name="Manager")
        user.groups.add(group)
        user.save()
        return Response({"message":"User added to manager group"}, status.HTTP_201_CREATED)
    return Response(status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@manager_required
def remove_manager(request,userId):
    if request.method == 'DELETE':
        user = User.objects.get(pk=userId)
        group = Group.objects.get(name="Manager")
        user.groups.remove(group)
        user.save()
        return Response({"message":"User removed from manager group"}, status.HTTP_201_CREATED)
    return Response(status.HTTP_400_BAD_REQUEST)



@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
@manager_required
def delivery_crew(request):
    if request.method == 'GET':
        delivery_list = User.objects.filter(groups__name="Delivery crew")
        serialized_data = UserSerializer(delivery_list, many=True)
        return Response(serialized_data.data, status.HTTP_200_OK)
    if request.method == 'POST':
        serialized_data = UserGroupSerializer(data=request.data)
        if serialized_data.is_valid(raise_exception=True):
            user = User.objects.get(email=serialized_data.data.get('email'))
            group = Group.objects.get(name="Delivery crew")
            user.groups.add(group)
            user.save()
            return Response({"message":"User added to delivery crew"}, status.HTTP_201_CREATED)
    return Response(status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@manager_required
def remove_delivery_crew(request, userId):
    if request.method == 'DELETE':
        user = User.objects.get(pk=userId)
        group = Group.objects.get(name="Delivery crew")
        user.groups.remove(group)
        user.save()
        allocated_items = AllocateOrders.objects.filter(delivery_man=user)
        for item in allocated_items:
            item.delete()
        return Response({"message":"User removed from delivery crew"}, status.HTTP_201_CREATED)
    return Response(status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@manager_required
def update_daily_item(request):
    if request.method == 'POST':
        serialized_item = UpdateItemOfTheDaySerializer(data=request.data)
        if serialized_item.is_valid(raise_exception=True):
            serialized_item.save()
            return Response(serialized_item.validated_data, status.HTTP_201_CREATED)
    return Response(status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
@throttle_classes([TenCallsPerMin])
@permission_classes([IsAuthenticated])
def bookings(request):
    if request.method == 'GET':
        items = Booking.objects.all()
        items = paginate_items(request, items)
        serialized_item = BookingSerializer(items, many=True)
        return Response(serialized_item.data, status.HTTP_200_OK)
    
    if request.method == 'POST':
        if not request.user.groups.filter(name="Manager") or request.user.groups.filter(name="Delivery crew"):
            serialized_data = MenuItemSerializer(data=request.data)
            if serialized_data.is_valid():
                serialized_data.save()
                return Response(serialized_data.data, status.HTTP_201_CREATED)
        return Response({"message":"only customers allower"},status.HTTP_405_METHOD_NOT_ALLOWED)
    return Response(status.HTTP_400_BAD_REQUEST)
        


@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticated])
@throttle_classes([TenCallsPerMin])
def single_booking(request, bookingId):
    booking = Booking.objects.filter(pk=bookingId)
    if len(booking) <=0:
        return Response(status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serialized_item = BookingSerializer(booking)
        return Response(serialized_item.data, status.HTTP_200_OK)
    
    if len(request.user.groups.filter(name="Manager")) <=0 and len(request.user.groups.filter(name="Manager"))<=0:
        if request.method == 'PUT':
            serialized_item = BookingSerializer(booking, data=request.data)
            if serialized_item.is_valid():
                serialized_item.save()
                return Response(serialized_item.data, status.HTTP_200_OK)
        if request.method == 'DELETE':
            booking.delete()
            return Response(status.HTTP_200_OK)
    else:
        return Response(status.HTTP_403_FORBIDDEN)
    return Response(status.HTTP_400_BAD_REQUEST)

# def register(request):
#     if request.method == 'POST':
#         data = json.load(request)

#         response = post('https://localhost:8000/auth/users', {
#             "email": data['email'],
#             "username": data['username'],
#             "password": data['password']
#         }).json()

#         if response.get('email') == data['email']:
#             return HttpResponse(request, response, content_type='application/json')
#         return HttpResponse('{"error": ')
