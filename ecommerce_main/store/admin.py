from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register([Categoric, Client, Type, Product, ItemStock, Order, OrderedItem, Adres, Banner, Color, Payment])