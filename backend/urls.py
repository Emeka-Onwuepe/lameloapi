from rest_framework import routers
from .Api import GetProducts, OrderView, PaymentView, LocationView, DashBoardView
# , GetProduct
from django.urls import path
router = routers.DefaultRouter()

urlpatterns = [
    path('getproducts', GetProducts.as_view(), name="getproducts"),
    path('orderview', OrderView.as_view(), name="Orderview"),
    path('payment', PaymentView.as_view(), name="payment"),
    path('location', LocationView.as_view(),
         name="location"),
    path('dashboard', DashBoardView.as_view(), name="dashboardview")
]

urlpatterns += router.urls
