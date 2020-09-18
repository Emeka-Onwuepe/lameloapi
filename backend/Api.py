from .serializer import (SizeSerializer, ProductSerializer, CategorySerializer, OrderedProductSerializer,
                         CustomerSerializer, OrderSerializer)
from .models import Size, Product, Category, OrderedProduct, Customer, Order
from rest_framework.response import Response
from rest_framework import generics


class GetProducts(generics.GenericAPIView):
    serializer_class = ProductSerializer

    def post(self, request, *args, **kwargs):
        action = request.data["action"]

        if action == "bfw":
            wants = ["burgers", "fries", "wings"]
            returned = []
            for item in wants:
                cat = Category.objects.get(name=item)
                # size = Size.objects.filter(multiplesizes__category__id=cat.id)
                # pureList = list(dict.fromkeys(size))
                # prices = SizeSerializer(pureList, many=True)
                products = ProductSerializer(cat.products, many=True)
                # , "prices": prices.data
                returned.append({item: products.data})
            return Response(returned)
        else:
            cat = Category.objects.get(name=action)
            product = cat.products
            # size = Size.objects.filter(multiplesizes__category__id=cat.id)
            # pureList = list(dict.fromkeys(size))
            # prices = SizeSerializer(pureList, many=True)
            products = ProductSerializer(product, many=True)
            # , "prices": prices.data
            return Response({action: products.data})


class GetProduct(generics.GenericAPIView):
    serializer_class = ProductSerializer

    def post(self, request, *args, **kwargs):
        product = Product.objects.get(id=int(request.data["id"]))
        size = Size.objects.filter(multiplesizes__id=product.id)
        cat = Category.objects.get(products=product)
        pro = Product.objects.filter(catproduct=cat.id).exclude(id=product.id)
        related = ProductSerializer(pro, many=True)
        prices = SizeSerializer(size, many=True)
        products = ProductSerializer(product)
        return Response({"product": products.data, "prices": prices.data, "related": related.data})
