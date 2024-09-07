from django.db import models
from django.contrib.auth.models import User


# Client
    # name
    # email
    # phone
    # user

# Categoric (Ex: Masculine, feminine, infant, etc.)
    # name

# Types (Ex: shirts, shorts, pants, etc)
    # name

# Product
    # image
    # name
    # price
    # active (cant delete the whole database if inactive as it would also delete all the history entries)
    # category
    # type

# Itemstock (different variations of the item)
    # product (Ex: shorts)
    # color
    # size (Ex: XL, L, M, etc)
    # quantity

# Order
    # client
    # end_date
    # finished
    # id_transaction
    # adress


# ItemsOrdered
    # itemstock (Ex: (short, black, XL))
    # quantity (Ex: 10)
    # order

# Adress
    # street
    # number
    # apartment
    # zip_code
    # city
    # state
    # client


# Create your models here.

class Client(models.Model): #? dont use plural names as django automatically puts a 's' after the name. Also a id is automatically created for each class
    name = models.CharField(max_length=200, null=True, blank=True) #? charfields are text fields. max_length determines the max number of characters
    email = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    id_session = models.CharField(max_length=200, null=True, blank=True)
    user = models.OneToOneField(User, null = True, blank = True, on_delete = models.CASCADE) #? each client can only be one user and one user can only be one client. Cascade deletes everyting associated to the user if its account is deleted

    def __str__(self) :
        return str(self.email)
    
class Categoric(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    slug = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self) :
        return str(self.name)

class Type(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    slug = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self) :
        return str(self.name)

class Product(models.Model):
    image = models.ImageField(null=True, blank=True) #? we will store the file name of the image so it can be accessed in the images folder, it generatea a url
    name = models.CharField(max_length=200, null=True, blank=True)
    price = models.DecimalField(max_digits = 7, decimal_places = 2, null=True, blank=True) #? max price is 99,999.99
    active = models.BooleanField(default=True)
    category = models.ForeignKey(Categoric, blank=True, null=True, on_delete=models.SET_NULL) #? primary key is a id associated to only that category,ForeignKey relates a category to another category with a diferent id. One product has only one category but one category has many products
    product_type = models.ForeignKey(Type, blank=True, null=True, on_delete=models.SET_NULL) #? When you delete a type or category, it will only set that product type to null, and not all the others when using CASCADE
    def __str__(self) :
        return f"Name: {self.name}, Category: {self.category}, Type: {self.product_type}, Price: {self.price}" 	

    def total_sales(self) :
        items = OrderedItem.objects.filter(order__finished=True, itemstock__product=self.id) #? obtaining the id of that specific item on the stock, as a itemstock contains one product, returns a list of those products
        total = sum([item.quantity for item in items])
        return total

class Color(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    code = models.CharField(max_length=200, null=True, blank=True) #? color code is a hex code

    def __str__(self) :
        return str(self.name)

class ItemStock(models.Model):
    product = models.ForeignKey(Product, blank=True, null=True, on_delete=models.SET_NULL) #? one itemstock is associated to a single product however one product can have many itemstocks
    color = models.ForeignKey(Color, blank=True, null=True, on_delete=models.SET_NULL)
    size = models.CharField(max_length=200, null=True, blank=True)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} - Color: {self.color} - Size: {self.size}"

class Adres(models.Model):
    street = models.CharField(max_length=200, null=True, blank=True)
    number = models.IntegerField(default=0)
    apartment = models.CharField(max_length=200, null=True, blank=True)
    zip_code = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    client = models.ForeignKey(Client, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return f"{self.client} - {self.street} - {self.city}"

class Order(models.Model):
    client = models.ForeignKey(Client, blank=True, null=True, on_delete=models.SET_NULL)
    end_date = models.DateTimeField(null=True, blank=True)
    finished = models.BooleanField(default=False)
    id_transaction = models.CharField(max_length=200, null=True, blank=True)
    adress = models.ForeignKey(Adres, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Client: {self.client} - id_order: {self.id} - Finalized: {self.finished}"

    @property
    def total_quantity(self) :
        items_ordered = OrderedItem.objects.filter(order__id = self.id) #? gets all the items of the order
        total_quantity = sum([item.quantity for item in items_ordered])
        return total_quantity
    
    @property
    def total_cost(self) :
        items_ordered = OrderedItem.objects.filter(order__id = self.id) #? gets all the items of the order
        total_cost = sum([item.total_price for item in items_ordered])
        return total_cost

    @property
    def items(self) :
        items_ordered = OrderedItem.objects.filter(order__id = self.id) #? gets all the items of the order
        return items_ordered



class OrderedItem(models.Model):
    itemstock = models.ForeignKey(ItemStock, blank=True, null=True, on_delete=models.SET_NULL)
    quantity = models.IntegerField(default=0)
    order = models.ForeignKey(Order, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Order ID: {self.order.id} - Product: {self.itemstock.product}, {self.itemstock.size}, {self.itemstock.color.name}"

    @property
    def total_price(self) :
        return self.quantity * self.itemstock.product.price

class Banner(models.Model) :
    image = models.ImageField(null=True, blank=True)
    link_output = models.CharField(max_length=400, null=True, blank=True) #? where the user will be sent after clicking the banner
    active = models.BooleanField(default=False) #? whether the link is currently active or not

    def __str__(self):
        return f"{self.link_output} - Active: {self.active}"

class Payment(models.Model) :
    payment_id = models.CharField(max_length=400)
    order = models.ForeignKey(Order, blank=True, null=True, on_delete=models.SET_NULL)
    aproved = models.BooleanField(default=False) 