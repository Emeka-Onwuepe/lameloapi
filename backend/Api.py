from .serializer import (SizeSerializer, ProductSerializer, CategorySerializer, LocationSerializer,
                         CustomerSerializer, OrderedSerializer, OrderedProductSerializer, ToppingSerializer,
                         ToppingsCollectionSerializer, GetOrderedSerializer, OrderedToppingSerializer)
from .models import Size, Product, Category, Customer, OrderedProduct, Ordered, Location, Topping, ToppingsCollection, OrderedTopping
from rest_framework.response import Response
from rest_framework import generics
from django.core.mail import send_mail
emailReciever = "pascalemy2010@gmail.com"


class GetProducts(generics.GenericAPIView):
    serializer_class = ProductSerializer

    def post(self, request, *args, **kwargs):
        action = request.data["action"]

        if action == "bfw":
            wants = ["burgers", "fries", "wings"]
            productList = []
            priceList = []
            for item in wants:
                cat = Category.objects.get(name=item)
                size = Size.objects.filter(multiplesizes__category__id=cat.id)
                pureList = list(dict.fromkeys(size))
                prices = SizeSerializer(pureList, many=True)
                products = ProductSerializer(cat.products, many=True)
                for item in products.data:
                    productList.append(item)
                for item in prices.data:
                    priceList.append(item)
            return Response({"products": productList, "prices": priceList})
        elif request.data["search"] == "orderedproducts":
            data = request.data["data"]
            toppingsData = []
            productQuery = OrderedProduct.objects.filter(purchaseId=int(data))
            products = OrderedProductSerializer(productQuery, many=True)
            try:
                toppingQuery = OrderedTopping.objects.filter(
                    purchaseId=int(data))
                toppings = OrderedToppingSerializer(
                    toppingQuery.toppings, many=True)
                toppingsData = toppings.data
            except Exception:
                pass
            return Response({"products": products.data, "toppings": toppingsData})
        else:
            cat = Category.objects.get(name=action)
            product = cat.products
            size = Size.objects.filter(multiplesizes__category__id=cat.id)
            pureList = list(dict.fromkeys(size))
            prices = SizeSerializer(pureList, many=True)
            products = ProductSerializer(product, many=True)
            toppingsData = ''
            try:
                toppingQuery = ToppingsCollection.objects.get(name=action)
                toppings = ToppingSerializer(toppingQuery.toppings, many=True)
                toppingsData = toppings.data
            except Exception:
                pass
            return Response({"products": products.data, "prices": prices.data, "toppings": toppingsData})


class OrderView(generics.GenericAPIView):
    serializer_class = CustomerSerializer

    def post(self, request, *args, **kwargs):
        userData = request.data['user']
        orderedData = request.data['Ordered']
        orderedProductData = request.data['OrderedProduct']
        userId = request.data["User"]
        orderedtoppings = request.data['OrderedToppings']
        # toppingIds = request.data["toppingIds"]
        serializer = ""
        if userId != "":
            customer = Customer.objects.get(id=int(userId))
            serializer = self.get_serializer(
                instance=customer, data=userData, partial=True)
        else:
            serializer = self.get_serializer(data=userData)
        serializer.is_valid(raise_exception=True)
        updatedUser = serializer.save()
        user = self.get_serializer(updatedUser)

        Ordered = OrderedSerializer(data=request.data['Ordered'], context={
                                    "customer": updatedUser})
        Ordered.is_valid(raise_exception=True)
        order = Ordered.save()
        Order = GetOrderedSerializer(order)

        # toppings
        # toppings = []
        # for items in toppingIds:
        #     item = Topping.objects.get(int(items))
        #     toppings.append(item)

        OrderedProduct = OrderedProductSerializer(
            data=orderedProductData, many=True, context={"purchaseId": order})
        OrderedProduct.is_valid(raise_exception=True)
        orderedproduct = OrderedProduct.save()

        if len(orderedtoppings) > 0:
            Orderedtoppings = OrderedToppingSerializer(
                data=orderedtoppings, many=True, context={"purchaseId": order})
            Orderedtoppings.is_valid(raise_exception=True)
            Orderedtoppings = Orderedtoppings.save()

        # prepare and send email

        # remember to add toppings to the list

        # tableHead = f'<table><thead><tr><th>Product Name</th><th>Size</th><th>Qty</th><th>Price</th></tr></thead>'
        # tableFoot = f'<tfoot><tr><td colspan="4">Total</td><td>&#x20A6; {orderedData["total"]}</td></tr></tfoot></table>'
        # products = ""
        # for item in orderedProductData:
        #     products += f'<tr><td>{item["name"]}</td><td>{item["size"]}</td><td>{item["quantity"]}</td><td>&#x20A6; {item["price"]}</td></tr>'
        # productTable = f"{tableHead}{products}{tableFoot}"
        # message = f"<p>You have a new order with the ID:<strong>{orderedData['OrderId']}</strong> and a total amount of <strong>&#x20A6; {orderedData['total']}</strong>.</p>"
        # message += f"<p>The ordered Product(s) is/are as follows: <br/>{productTable}</p><p>{updatedUser} contact detail is as follows:<br/>"
        # message += f"Email: {updatedUser.email} <br/> Phone Number:{updatedUser.phoneNumber} <br/> Address:{updatedUser.address}</p>"
        # send_mail(f"New Order from {updatedUser}", "", "Peastan", [
        #           emailReciever], fail_silently=False, html_message=message)
        return Response({"Ordered": Order.data, "user": user.data})


class PaymentView(generics.GenericAPIView):
    serializer_class = OrderedSerializer

    def post(self, request, *args, **kwargs):
        orderedID = request.data['id']
        orderedObj = Ordered.objects.get(id=int(orderedID))
        orderedObj.paid = True
        orderedObj.save()
        returnedData = GetOrderedSerializer(orderedObj)
        return Response(returnedData.data)


class LocationView(generics.GenericAPIView):
    serializer_class = LocationSerializer

    def get(self, request, *args, **kwargs):
        locations = Location.objects.all()
        # toppings = Topping.objects.all()
        # toppingdata = ToppingSerializer(toppings, many=True)
        serializer = self.get_serializer(locations, many=True)
        return Response(serializer.data)


class DashBoardView(generics.GenericAPIView):
    serializer_class = GetOrderedSerializer

    def get(self, request, *args, **kwargs):
        ordered = Ordered.objects.filter(paid=True).filter(archived=False)
        orderdSerializer = GetOrderedSerializer(ordered, many=True)
        customer = Customer.objects.all()
        customerData = CustomerSerializer(customer, many=True)
        return Response({"ordered": orderdSerializer.data, "customers": customerData.data})

    def post(self, request, *args, **kwargs):
        if request.data["search"] == "orderedproducts":
            data = request.data["data"]
            customerID = request.data["customer"]
            productQuery = OrderedProduct.objects.filter(purchaseId=int(data))
            products = OrderedProductSerializer(productQuery, many=True)
            customer = Customer.objects.get(id=int(customerID))
            customerData = CustomerSerializer(customer)
            toppingsData = []
            # try:
            toppingQuery = OrderedTopping.objects.filter(
                purchaseId=int(data))
            toppings = OrderedToppingSerializer(
                toppingQuery.toppings, many=True)
            toppingsData = toppings.data
            # except Exception:
            #     pass
            return Response({"products": products.data, "customer": customerData.data})
        elif request.data["action"] == "Get_Archive":
            ordered = Ordered.objects.filter(archived=True)
            orderdSerializer = GetOrderedSerializer(ordered, many=True)
            customer = Customer.objects.all()
            customerData = CustomerSerializer(customer, many=True)
            return Response({"Archive": orderdSerializer.data, "customers": customerData.data, "toppings": toppingsData})
        else:
            if request.data["action"] == "Delivered":
                data = request.data["data"]
                order = Ordered.objects.get(OrderId=data)
                order.delivered = True
                order.save()
            elif request.data["action"] == "Archive":
                data = request.data["data"]
                order = Ordered.objects.get(OrderId=data)
                order.archived = True
                order.save()
            ordered = Ordered.objects.filter(paid=True).filter(archived=False)
            orderdSerializer = GetOrderedSerializer(ordered, many=True)
            customer = Customer.objects.all()
            customerData = CustomerSerializer(customer, many=True)
            return Response({"ordered": orderdSerializer.data, "customers": customerData.data})
