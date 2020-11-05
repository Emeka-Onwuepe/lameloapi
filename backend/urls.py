from rest_framework import routers
from .Api import GetProducts, OrderView, PaymentView, LocationView, DashBoardView, LoginUser
# , GetProduct
from django.urls import path
from knox import views as KnoxView
router = routers.DefaultRouter()

urlpatterns = [
    path('login', LoginUser.as_view(), name="login"),
    path('logout', KnoxView.LogoutView.as_view(), name="knox_logout"),
    path('getproducts', GetProducts.as_view(), name="getproducts"),
    path('orderview', OrderView.as_view(), name="Orderview"),
    path('payment', PaymentView.as_view(), name="payment"),
    path('location', LocationView.as_view(),
         name="location"),
    path('dashboard', DashBoardView.as_view(), name="dashboardview")
]

urlpatterns += router.urls
