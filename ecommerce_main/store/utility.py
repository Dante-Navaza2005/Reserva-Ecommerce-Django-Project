from django.db.models import Max, Min
from django.core.mail import send_mail


def filter_product(products, filter):
    if filter:
        if "-" in filter:
            category, product_type = filter.split("-")
            products = products.filter(category__slug = category, product_type__slug = product_type) 
            #? ABOVE gets the slug atribute from the category and product_type (in the database relationship it is described that way)class and filters it according to the name of the category obtained from the url
        else: #? client only filtered by the category
            products = products.filter(category__slug = filter) #? gets the slug atribute from the category class and filters it according to the name of the category obtained from the banner
    return products

def min_max_price (products) :
    min_price = 0
    max_price = 0

    if (len(products) > 0) : #? rounding function doesnt work for NaN values
        min_price = list(products.aggregate(Min("price")).values())[0] #? obtaining the maximum price (attribute from the Product class)
        max_price = list(products.aggregate(Max("price")).values())[0] #? obtaining the maximum price (attribute from the Product class)
        min_price = round(min_price, 2) #? rounding to two decimal places
        max_price = round(max_price, 2) #? rounding to two decimal places
    
    return min_price, max_price

def order_products(products, order) :
    if order == "highest-price" :
        products = products.order_by("-price")
    elif order == "lowest-price" :
        products = products.order_by("price")
    elif order == "most-sold" :
        product_list = []
        for product in products :
            product_list.append((product.total_sales(), product)) #? saved the quantity on the first position of the tuple list since sorted can order it based on the first index
        product_list = sorted(product_list, reverse=True, key=lambda tuple: tuple[0])
        products = [item[1] for item in product_list] #? grabbing the product from the ordered tuple list
        
    return products

def secure_password(password: str) :
    if len(password) < 8 or len(password) > 20:
        return False
    special_characters = set('" "!@#$%^&*()-+?_=,<>/""''|.;:')
    has_lower = has_upper = has_number = has_special = False

    for character in password:
        if character.islower():
            has_lower = True
        elif character.isupper():
            has_upper = True
        elif character.isdigit():
            has_number = True
        elif character in special_characters:
            has_special = True
        
        if has_lower and has_upper and has_number and has_special:
            return True

    return False

def send_purchase_email(order) :
        email = order.client.email
        subject = f"Order Approved {order.id}"
        items_summary = '\n'.join([
    f"Product: {item.itemstock.product.name}, Unitary Price: R$ {item.itemstock.product.price}, Size: {item.itemstock.size}, Quantity: {item.quantity}, Color: {item.itemstock.color.name}, Total product price: R$ {item.total_price}"
    for item in order.items
])
        body = f"""Congratulations! Your order was approved.
        Order ID: {order.id}
        FInal order price: R$ {order.total_cost}
        Order Content: 
        {items_summary}
        Total Quantity: {order.total_quantity}"""
        
        sender = "dantenavaza2005@gmail.com"
        send_mail(subject, body, sender, [email]) #? email must be in list