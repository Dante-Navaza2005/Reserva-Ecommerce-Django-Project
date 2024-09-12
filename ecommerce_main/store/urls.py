from django.urls import path
from .views import * #? Importing everything from the views folder in the same directory
from django.contrib.auth import views

urlpatterns = [
    path('', homepage, name="homepage"), #? first parameter is the url, second is what function will be runned at the url, and the third is the internal name of the link used to reference the link regardless of its url domain
    path('store/', store, name="store"),
    
    path('store/<str:filter>/', store, name="store"), #? comes after the fixed urls, allows to create multiple urls with varied names
    path('product/<int:product_id>/', view_product, name="view_product"),
    path('product/<int:product_id>/<int:id_color>/', view_product, name="view_product"),
    
    path('cart/', cart, name="cart"), 
    path('checkout/', checkout, name="checkout"), 
    path('addtocart/<int:product_id>/', add_to_cart, name="add_to_cart"),
    path('removefromcart/<int:product_id>/', remove_from_cart, name="remove_from_cart"),
    path('addaddress/',add_address, name="add_address"),
    path('finishorder/<int:order_id>/',finish_order, name="finish_order"),
    path('finalizepayment/',finalize_payment, name="finalize_payment"),
    path('orderaproved/<int:order_id>/',order_aproved, name="order_aproved"),
    
    path('youraccount/', your_account, name="your_account"),  #? separated for organization purposes
    path('myorders/', my_orders, name="my_orders"),  
    path('performlogin/', perform_login, name="perform_login"), 
    path('createaccount/', create_account, name="create_account"),
    path('performlogout/', perform_logout, name="perform_logout"),

    path('managestore/', manage_store, name="manage_store"),
    path('exportreport/<str:report>/', export_report, name="export_report"),

    path("password_change/", views.PasswordChangeView.as_view(), name="password_change"),
    path("password_change/done/", views.PasswordChangeDoneView.as_view(), name="password_change_done"),
    
    path("password_reset/", views.PasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/", views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

]