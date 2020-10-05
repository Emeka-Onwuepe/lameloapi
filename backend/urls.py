from rest_framework import routers
from .Api import GetProducts, OrderView, PaymentView, LocationAndTopingView
# , GetProduct
from django.urls import path
router = routers.DefaultRouter()

urlpatterns = [
    path('getproducts', GetProducts.as_view(), name="getproducts"),
    path('orderview', OrderView.as_view(), name="Orderview"),
    path('payment', PaymentView.as_view(), name="payment"),
    path('Locationandtoping', LocationAndTopingView.as_view(),
         name="locationandtopingview")
]

urlpatterns += router.urls
