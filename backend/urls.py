from rest_framework import routers
from .Api import GetProducts, GetProduct
from django.urls import path
router = routers.DefaultRouter()

urlpatterns = [
    path('getproducts', GetProducts.as_view(), name="getproducts"),
    path('getproduct', GetProduct.as_view(), name="getproduct"),
]

urlpatterns += router.urls
