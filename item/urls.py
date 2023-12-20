from django.urls import include,path
from . import views
urlpatterns=[
    path('client/',views.client,name="client"),
    path('cussin/',views.cussin,name="cussin"),
    path('cart/',views.cart,name="cart"),
    path('cart-ele/',views.cart1,name="cart1"),
    path('price/',views.price,name="price"),
    path('placeorder/',views.placeorder,name="placeorder"),
    path('check/',views.check,name="check"),
    path('checkout/',views.checkout,name="checkout"),
  # path("add_to_cart", views.add_to_cart, name= "add"),
]