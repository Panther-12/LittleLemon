from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from api.models import MenuItems
from django.core import serializers
from .models import Booking
from datetime import datetime
import json
from .forms import BookingForm

def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')


def book(request):
    # form = BookingForm()
    # if request.method == 'POST':
    #     form = BookingForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    # context = {'form':form}
    return render(request, 'book.html')

@csrf_exempt
def update_slots(request):
    if request.method == 'POST':
        data = json.load(request)
        date_exist = Booking.objects.filter(reservation_date=data['reservation_date'])
        slot_exist = date_exist.filter(reservation_slot=data['reservation_slot']).exists()
        if slot_exist == False:
            booking = Booking(first_name=data['first_name'], reservation_date=data['reservation_date'], reservation_slot=data['reservation_slot'])
            booking.save()
        return HttpResponse("{'error':1}", content_type="application/json")
    
    date = request.GET.get('date',datetime.today().date())
    bookings = Booking.objects.filter(reservation_date=date).order_by('reservation_date')
    booking_json = serializers.serialize('json',bookings) # For the normal serializer in django
    # you have to specify the type of data produced by the serializer
    return HttpResponse(booking_json, content_type="application/json")

@csrf_exempt
def bookings(request):
    bookings = Booking.objects.all()
    booking_json = serializers.serialize('json',bookings) # For the normal serializer in django
    # you have to specify the type of data produced by the serializer
    return render(request, 'bookings.html', {'bookings':booking_json})

@csrf_exempt
def specific_date_bookings(request, date):
    if request.method == 'GET':
        bookings = Booking.objects.filter(reservation_date=date)
        booking_json = serializers.serialize('json',bookings) # For the normal serializer in django
        # you have to specify the type of data produced by the serializer
        return HttpResponse(booking_json, content_type="application/json")
    return HttpResponse('{"400 Bad Request":1}', content_type="application/json")


def menu(request):
    menu_data = MenuItems.objects.all()
    main_data = {"menu": menu_data}
    return render(request, 'menu.html', {"menu": main_data})


def display_menu_item(request, pk=None): 
    if pk: 
        menu_item = MenuItems.objects.get(pk=pk) 
    else: 
        menu_item = "" 
    return render(request, 'menu_item.html', {"menu_item": menu_item}) 