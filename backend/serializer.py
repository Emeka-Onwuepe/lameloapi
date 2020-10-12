from rest_framework import serializers
from .models import Size, Product, Category, Customer, Ordered, OrderedProduct, Location, Topping, ToppingsCollection


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"

class GetOrderedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ordered
        fields = "__all__"


class OrderedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ordered
        # fields = "__all__"
        exclude = ["customer"]

    def create(self, validated_data):
        customer = self.context.get("customer")
        order = Ordered.objects.create(
            OrderId=validated_data["OrderId"], customer=customer, destination=validated_data["destination"],
            logistics=validated_data["logistics"], total=validated_data["total"])
        order.save()
        return order


class OrderedProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderedProduct
        fields = ["id", "name",
                  "quantity", "price", "size", "product"]

    def create(self, validated_data):
        purchaseId = self.context.get("purchaseId")
        # toppings = self.context.get("toppings")

        Product = OrderedProduct.objects.create(name=validated_data["name"],
                                                quantity=validated_data["quantity"], price=validated_data["price"],
                                                size=validated_data["size"],
                                                purchaseId=purchaseId, product=validated_data["product"])
        Product.save()
        # for item in toppings:
        #     Product.toppings.add(int(item))
        # return Product


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class ToppingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topping
        fields = "__all__"


class ToppingsCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToppingsCollection
        fields = "__all__"
