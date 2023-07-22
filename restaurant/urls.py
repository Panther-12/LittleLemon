from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('book/', views.book, name="book"),
    path('menu/', views.menu, name="menu"),
    path('menu_item/<int:pk>/', views.display_menu_item, name="menu_item"),  
    path('bookings-r/', views.bookings, name="bookings-r"),
    path('bookings/<str:date>/', views.specific_date_bookings, name="specific_date_bookings"),
    path('update-slots/', views.update_slots, name="update-slots"),
]