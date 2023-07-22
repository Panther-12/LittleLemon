from django.urls import path
from . import views 
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    # Add app urls here
    path('menu-items/', views.menu_items, name="menu_items"),
    path('menu-items/<int:menuItem>', views.single_item, name='single_item'),
    path('category/', views.category, name="category"),
    path('orders/', views.orders, name="orders"),
    path('orders/<int:orderId>/', views.single_order, name='single_order'),
    path('bookings/', views.bookings, name="bookings"),
    path('bookings/<int:bookingId>/', views.single_booking, name='single_booking'),
    path('cart/menu-items/', views.cart, name="cart"),
    path('groups/manager/users/', views.managers, name="managers"),
    path('groups/manager/users/<int:userId>', views.remove_manager, name="remove-manager"),
    path('groups/delivery-crew/users/', views.delivery_crew, name="delivery_crew"),
    path('groups/delivery-crew/users/<int:userId>', views.remove_delivery_crew, name="remove-delivery-crew"),
    path('item-of-the-day/', views.update_daily_item, name="update-daily-item"),
    path('api-token-auth/', obtain_auth_token, name="obtain-token")
    # auth/users - GET if admin lists all users in the system
    #            - POST creates a new user provided username and password
    # auth/token/login - POST if username and password provided it creates a token for the user
    # auth/token/logout - Deletes the current users token
]