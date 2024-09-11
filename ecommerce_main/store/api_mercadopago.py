import mercadopago

public_key = "APP_USR-8e9c2811-1d99-4346-b8a0-9118201f7216"
access_token = "APP_USR-1378561128003766-083016-a08284dad9da4451cc196354af9f6722-1968090813"

def create_payment(items_ordered, link) :
    #configure your credentials
    sdk = mercadopago.SDK(access_token) #? validating access token

    #? items the user is purchasing
    items = []
    for item in items_ordered :
        quantity = int(item.quantity)
        product_name = item.itemstock.product.name
        unit_price = float(item.itemstock.product.price)
        items.append({
            "title": product_name, 
            "quantity": quantity, 
            "unit_price": unit_price
            })

    # Create items in the preference. preference = personalized charge for clients
    preference_data = {
        "items": items,
        "auto_return": "all", #? auto-return to site after payment  
        "back_urls": { #? links that will be loaded in each payment cenario
            "success": link,
            "failure": link,
            "pending": link,
        }, 
    }

    # Create a preference
    preference_response = sdk.preference().create(preference_data) #? creating request with various informations about the payment
    payment_link = preference_response["response"]["init_point"]
    payment_id = preference_response["response"]["id"] #? obtaining the payment id to treat it
    return payment_link, payment_id