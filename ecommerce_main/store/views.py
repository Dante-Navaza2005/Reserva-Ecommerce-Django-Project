from django.shortcuts import render, redirect
from .models import *
import uuid
from .utility import filter_product, min_max_price, order_products, secure_password, send_purchase_email
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from datetime import datetime
from .api_mercadopago import create_payment #? needs to put the point so it searches on the same folder
from django.urls import reverse

# Create your views here.
def homepage(request): #? the first parameter always has to be a request
    banners = Banner.objects.filter(active=True)
    context = {"banners" : banners}
    return render(request, 'homepage.html', context) #? returns the homepage

def store(request, filter = None):
    products = Product.objects.filter(active=True) #? grabbing all products from the database (queryset, result of the search of the database)
    products = filter_product(products, filter) #? using the filter_product function to split the url from '-'

    #! Applying the filters from the form
    if request.method == 'POST':
        data = request.POST.dict() #? converts the request data to a dictionary
        products = products.filter(price__gte=data.get('min_price'), price__lte=data.get('max_price'))
        if "size" in data :
            items = ItemStock.objects.filter(product__in=products, size=data.get('size')) 
            id_product = items.values_list("product", flat=True).distinct()
            products = products.filter(id__in=id_product)
        if "type" in data :
            products = products.filter(product_type__slug=data.get('type'))
        if "category" in data :
            products = products.filter(category__slug=data.get('category'))

    items = ItemStock.objects.filter(quantity__gt=0, product__in=products) #? getting the items of that product that have a quantity greater than 0
    sizes = items.values_list("size", flat=True).distinct() #? getting the sizes of the items, flat parameter makes it return a single-column list of values instead of tuple
    
    #? making only the available categories and types appear
    id_type = products.values_list("product_type", flat=True).distinct()
    types = Type.objects.filter(id__in=id_type)
    id_categories = products.values_list("category", flat=True).distinct()
    categories = Categoric.objects.filter(id__in=id_categories)

    
    min_price, max_price = min_max_price(products)

    #! Changing the order of the products
    order = request.GET.get('order') #? gets the parameter value of 'order'
    products = order_products(products, order)

    context = {"products" : products, "min_price" : min_price, "max_price" : max_price, "sizes" : sizes, "categories" : categories, "types" : types} 
    return render(request, 'store.html', context) 

def add_to_cart(request, product_id):
    if request.method == "POST" and product_id : #? if the user is sending a new product
        data = request.POST.dict() #? converts the request data to a dictionary
        size = data.get('size') #? used get instead of ['size'] as it wont return a error
        color_id = data.get('color')
        if not size: #? only check the size as it only appears after selecting the color
            return redirect('store')
        
        #!getting the client
        answer = redirect('cart') #? to implement cookies we need to edit the redirect response
        if request.user.is_authenticated:
            client = request.user.client
        else :
            if request.COOKIES.get("id_session") : #? checks if there is already a registred anonymous session
                id_session = request.COOKIES.get("id_session")
            else :
                id_session = str(uuid.uuid4()) #? uuid4 guarantees uniqueness and safety
                answer.set_cookie(key="id_session", value=id_session, max_age=60*60*24*40) #? max age in seconds
            client, created = Client.objects.get_or_create(id_session=id_session) 
            
        order, created = Order.objects.get_or_create(client=client, finished=False)
        item_stock = ItemStock.objects.get(product__id=product_id, size=size, color=color_id) #? In the forms we enter the color, id, and the size
        item_ordered, created = OrderedItem.objects.get_or_create(order=order, itemstock=item_stock) #? adding the product to the cart
        item_ordered.quantity += 1
        item_ordered.save() #? Must save changes made directly to a element
        return answer
    else :
        return redirect('store') #? redirect the user to the store if he didn't choose a product

def remove_from_cart(request, product_id) :
    if request.method == "POST" and product_id : #? if the user is sending a new product
        data = request.POST.dict() #? converts the request data to a dictionary
        size = data.get('size') #? used get instead of ['size] as it wont return a error
        color_id = data.get('color')
        if not size:
            return redirect('store')
        #!getting the client
        if request.user.is_authenticated:
            client = request.user.client
        else :
            if request.COOKIES.get('id_session') :
                id_session = request.COOKIES.get("id_session")
                client, created = Client.objects.get_or_create(id_session=id_session)
            else : #? if the client enters directly on the cart, whithout generating cookies
                return redirect('store') #? return directly to the store as the cart should be empty
        order, created = Order.objects.get_or_create(client=client, finished=False)
        item_stock = ItemStock.objects.get(product__id=product_id, size=size, color=color_id) #? In the forms we enter the color, id, and the size
        item_ordered, created = OrderedItem.objects.get_or_create(order=order, itemstock=item_stock) #? adding the product to the cart
        item_ordered.quantity -= 1 #? only difference is that we are removing a item from the cart
        item_ordered.save() #? Must save changes made directly to a element
        if item_ordered.quantity <= 0 :
            item_ordered.delete()
        return redirect('cart')
    else :
        return redirect('store') #? redirect the user to the store if he didn't choose a product

def cart(request):
    #! getting the client
    if request.user.is_authenticated:
        client = request.user.client
    else :
        if request.COOKIES.get('id_session') :
            id_session = request.COOKIES.get("id_session")
            client, created = Client.objects.get_or_create(id_session=id_session)
        else : #? if the client enters directly on the cart, whithout generating cookies
            context = {"existing_client": False, "order" : None, "items_ordered" : None}
            return render(request, 'cart.html', context) 
    order, created = Order.objects.get_or_create(client=client, finished=False) 
    items_ordered = OrderedItem.objects.filter(order = order)
    context = {"order" : order, "items_ordered" : items_ordered, "existing_client": True}
    return render(request, 'cart.html', context) 

def checkout(request): 
    #! getting the client
    if request.user.is_authenticated:
        client = request.user.client
    else :
        if request.COOKIES.get('id_session') :
            id_session = request.COOKIES.get("id_session")
            client, created = Client.objects.get_or_create(id_session=id_session)
        else : #? if the client enters directly on the cart, whithout generating cookies
            return redirect('store') #? return directly to the store as the cart should be empty
    order, created = Order.objects.get_or_create(client=client, finished=False) 
    addresses = Adres.objects.filter(client=client) #? filters all adresses associated with the client
    context = {"order" : order, "addresses" : addresses, "error" : None}
    return render(request, 'checkout.html', context) 

def finish_order(request, order_id) :
    if request.method == "POST" :
        error = None
        data = request.POST.dict()
        total = data.get("total")
        order = Order.objects.get(id=order_id) #? used get because it is only one order

        total = total.replace(",",".") #? in case you are using brazilian version
        if float(total) != float(order.total_cost) : #? transformed to float to avoid comparisson errors
            error = "conflicting_cost" #? in case the user tries to manipulate the html

        if not "adress" in data :
            error = "adress"
        else :
            id_adress = data.get("adress")
            adress = Adres.objects.get(id=id_adress)
            order.adress = adress
        
        if not request.user.is_authenticated :
            email = data.get("email")
            try :
                validate_email(email)
            except ValidationError :
                error = "email"
            if not error :
                clients = Client.objects.filter(email=email)
                if clients:
                    order.client = clients[0]
                else:
                    order.client.email = email
                    order.client.save()
        
        id_transaction = f"{order.id}-{datetime.now().timestamp()}"
        order.id_transaction = id_transaction
        order.save()

        if error :
            addresses = Adres.objects.filter(client=order.client) #? filters all adresses associated with the client
            context = {"error" : error, "order" : order, "addresses" : addresses}
            return render(request,"checkout.html", context)
        else :
            #? make payment
            items_ordered = OrderedItem.objects.filter(order=order)
            link = request.build_absolute_uri(reverse("finalize_payment"))
            payment_link, payment_id= create_payment(items_ordered, link)
            payment = Payment.objects.create(payment_id=payment_id,order=order)
            payment.save()
            return redirect(payment_link)
    else :
        return redirect("store")

def finalize_payment(request) :
    data = request.GET.dict()
    status = data.get("status")
    payment_id = data.get("preference_id")
    if status == "approved" :
        payment = Payment.objects.get(payment_id=payment_id) #? getting the already existing payment
        payment.aproved = True
        order = payment.order
        order.finished = True
        order.end_date = datetime.now()
        order.save()
        payment.save()

        #? email system
        send_purchase_email(order)
        

        if request.user.is_authenticated :
            return redirect("my_orders") #? show finished orders
        else :
            return redirect("order_aproved", order.id)
    else :
        return redirect("checkout")

def order_aproved(request, order_id) :
    order = Order.objects.get(id=order_id) #? getting the order by its id
    context = {"order" : order}
    return render(request, "order_aproved.html", context)

# TODO error when finishing order after aunathenticades user address

def add_address(request) :
    if request.method == "POST" : #? handling the submission of the form
        if request.user.is_authenticated:
            client = request.user.client
        else :
            if request.COOKIES.get('id_session') :
                id_session = request.COOKIES.get("id_session")
                client, created = Client.objects.get_or_create(id_session=id_session)
            else : #? if the client enters directly on the cart, whithout generating cookies
                return redirect('store') #? return directly to the store as the cart should be empty
        data = request.POST.dict() #? converts the request data to a dictionary
        address = Adres.objects.create(client=client, street=data.get('street'), city=data.get('city'), state=data.get('state'), zip_code=data.get('zip_code'), number=int(data.get('number')), apartment=data.get('apartment'))
        address.save()
        return redirect('checkout') #? redirects the user to the checkout page to add more addresses if needed
    else :
        context = {}
        return render(request, 'add_address.html', context)


def view_product(request, product_id, id_color = None) :
    has_stock = False
    sizes = {}
    colors = {} #? needs to be declared
    selected_color = None
    product = Product.objects.get(id=product_id) #? id parameter is created automatically by django
    item_stock = ItemStock.objects.filter(product = product, quantity__gt = 0) #? gets the product that has more than 0 quantity (queryset lookup)
    if len(item_stock) > 0 : 
        has_stock = True #? necessary in order to do a if on the html. if the product is out of stock, will show "Out of Stock"
        colors = {item.color for item in item_stock} #? gets the colors of all products, uses sets '{}' to avoid duplicate colors
        if id_color :
            selected_color = Color.objects.get(id = id_color) #? gets the color object from the Color class
            item_stock = ItemStock.objects.filter(product = product, quantity__gt = 0, color__id = id_color) #? gets the color id  attribute from the Color class (that is automatically created)
            sizes = {item.size for item in item_stock} #? gets the sizes of all products
    context = {'product': product, "has_stock" : has_stock, "colors" : colors, "sizes" : sizes, "selected_color" : selected_color}
    return render(request, 'view_product.html', context)

def create_account(request):
    error = None
    if request.user.is_authenticated:
        return render(request, 'user/create_account.html')
    
    if request.method == "POST":
        data = request.POST.dict()
        email = data.get("email", "").strip()  # Ensure email is stripped of whitespace
        password = data.get("password")
        confirm_password = data.get("confirm_password")
        
        if email and password and confirm_password:  # Check if all fields are filled
            try:
                validate_email(email)  # Validate email format
            except ValidationError:
                error = "invalid_email"
            else:
                if secure_password(password) :
                    if password == confirm_password:
                        user, created = User.objects.get_or_create(username=email, email=email)
                        if not created:
                            error = "user_exists"
                        else:
                            user.set_password(password)
                            user.save()  # Save the user
                            
                            # Authenticate and log in the user
                            user = authenticate(request, username=email, password=password)
                            if user is not None:
                                login(request, user)
                                
                                # Handle client creation or update
                                id_session = request.COOKIES.get("id_session")
                                if id_session:
                                    client, created = Client.objects.get_or_create(id_session=id_session)
                                else:
                                    client, created = Client.objects.get_or_create(email=email)
                                client.user = user
                                client.email = email
                                client.save()
                                
                                return redirect('store')
                    else:
                        error = "different_password"
                else :
                    error = "weak_password"
        else:
            error = "fill"
    
    context = {"error": error}
    return render(request, 'user/create_account.html', context)

@login_required
def your_account(request):
    error = None
    altered_account = False
    altered_password = False
    if request.method == 'POST':
        data = request.POST.dict()
        #? email and password are outside to diferentiate what forms is submitted
        if data.get('current_password'):
            #? is modifying the password
            current_password = data.get("current_password")
            new_password = data.get("new_password")
            confirm_new_password = data.get("confirm_new_password")
            if current_password != new_password and confirm_new_password != current_password:
                if secure_password(new_password) :
                    if new_password == confirm_new_password :
                        #? verify current password
                        user = authenticate(request, username=request.user.email, password=current_password)
                        if user:
                            #? correct password, change password
                            user.set_password(new_password)
                            user.save()
                            altered_password = True
                        else :
                            error = "invalid_current_password"
                    else :
                        error = "different_passwords"
                else :
                    error = "weak_password"
            else :
                error = "same_password"

        elif data.get("email") : 
            #? is modifying the account data
            email = data.get("email")
            phone = data.get("phone")
            name = data.get("name")
            if email != request.user.email :
                users = User.objects.filter(email=email)
                if len(users) > 0 :
                    error = "email_exists"
            if not error :
                client = request.user.client
                client.email = email
                request.user.username = email
                request.user.email = email #? also changing from the user, they are different things
                client.name = name
                client.phone = phone
                client.save()
                request.user.save()
                altered_account = True
        else :
            error = "invalid_changes"

    context = {"error" : error, "altered_account" : altered_account, "altered_password" : altered_password}
    return render(request, 'user/your_account.html', context) 

@login_required
def my_orders(request):
    client = request.user.client #? gets the client associated with the current authenticated user user
    orders = Order.objects.filter(finished=True, client=client).order_by("-end_date") #? gets all finished orders associated with the client user in descending date order
    
    context = {"orders" : orders}
    return render(request, 'user/my_orders.html', context)

def perform_login(request):
    error = False
    if request.user.is_authenticated :
        return redirect('store')
    if request.method == "POST":
        data = request.POST.dict()
        if "email" in data and "password" in data :
            email = data.get("email")
            password = data.get("password")
            user = authenticate(request, username=email, password=password) #? authenticating the user
            if user :
                #? perform login
                login(request, user)
                return redirect('store')
            else :
                #? We used booleans as there is only one type of error,
                error = True
        else :
            error = True
    
    context = {"error" : error}
    return render(request, 'user/login.html', context)
@login_required
def perform_logout(request) :
    logout(request)
    return redirect('perform_login')

@login_required
def manage_store(request):
    return render(request,"internal/manage_store.html")

