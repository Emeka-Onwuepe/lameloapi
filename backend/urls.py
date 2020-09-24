from rest_framework import routers
from .Api import GetProducts, OrderView
# , GetProduct
from django.urls import path
router = routers.DefaultRouter()

urlpatterns = [
    path('getproducts', GetProducts.as_view(), name="getproducts"),
    path('orderview', OrderView.as_view(), name="Orderview"),
    # path('getproduct', GetProduct.as_view(), name="getproduct"),
]

urlpatterns += router.urls
