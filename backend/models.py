from django.db import models


class Size(models.Model):
    """Model definition for Size."""

    size = models.CharField(verbose_name="size", max_length=150)
    price = models.IntegerField(verbose_name="price")

    class Meta:
        """Meta definition for Size."""

        verbose_name = 'Size'
        verbose_name_plural = 'Sizes'

    def __str__(self):
        """Unicode representation of Size."""
        return f'{self.size}-{self.price}'


class Product(models.Model):
    """Model definition for Product."""

    name = models.CharField(verbose_name='name', max_length=200)
    image = models.ImageField(verbose_name="image", default="image")
    flavour = models.CharField(
        verbose_name="flavour", max_length=200, blank=True, default="null")
    description = models.TextField(verbose_name="description")
    price = models.IntegerField(verbose_name="price", blank=True, default=0)
    multipleSIzes = models.ManyToManyField(
        Size, verbose_name="multiplesizes", related_name="multiplesizes", blank=True)

    class Meta:
        """Meta definition for Product."""

        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        """Unicode representation of Product."""
        return self.name


class Category(models.Model):
    """Model definition for Category."""

    name = models.CharField(verbose_name="name", max_length=150)
    products = models.ManyToManyField(
        Product, verbose_name="products", blank=True)

    class Meta:
        """Meta definition for Category."""

        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        """Unicode representation of Category."""
        return self.name


class OrderedProduct(models.Model):
    """Model definition for OrderedProduct."""
    orderId = models.CharField(verbose_name="orderId", max_length=150)
    product = models.ForeignKey(
        Product, related_name="product", verbose_name="product", on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name="quantity")
    size = models.CharField(verbose_name="size", max_length=150)
    price = models.IntegerField(verbose_name="price")

    class Meta:
        """Meta definition for OrderedProduct."""

        verbose_name = 'OrderedProduct'
        verbose_name_plural = 'OrderedProducts'

    def __str__(self):
        """Unicode representation of OrderedProduct."""
        return self.orderId


class Customer(models.Model):
    """Model definition for Customer."""

    customerId = models.CharField(verbose_name="customer Id", max_length=100)
    fullName = models.CharField(verbose_name="full name", max_length=250)
    email = models.EmailField(verbose_name="email", max_length=254)
    phoneNumber = models.CharField(verbose_name="phone Number", max_length=50)

    class Meta:
        """Meta definition for Customer."""

        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    def __str__(self):
        """Unicode representation of Customer."""
        self.fullName


class Order(models.Model):
    """Model definition for Order."""

    orderId = models.CharField(verbose_name="orderId", max_length=150)
    orderProducts = models.ManyToManyField(
        OrderedProduct, verbose_name="orderedproducts", related_name="orderedproducts")
    customer = models.ForeignKey(
        Customer, verbose_name="customer", on_delete=models.CASCADE)

    class Meta:
        """Meta definition for Order."""

        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        """Unicode representation of Order."""
        return self.orderId
