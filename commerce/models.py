from django.db import models
from django.conf import settings
from accounts.models import User
from django.db.models import Sum, F

# Create your models here. (Users, orders, products, payments)
class Product(models.Model):
    CHOICES = (
        ("electronics", "Electronics"),
        ("fashion", "Fashion"),
        ("home_kitchen", "Home & Kitchen"),
        ("beauty_care", "Beauty & Personal Care"),
        ("sports_outdoors", "Sports & Outdoors"),
        ("health_wellness", "Health & Wellness"),
        ("automotive", "Automotive"),
        ("books_media", "Books & Media"),
        ("toys_games", "Toys & Games"),
        ("groceries", "Groceries"),
        ("office_supplies", "Office Supplies"),
        ("pet_supplies", "Pet Supplies"),
        ("others", "Others"),
    )

    # add owner field to track who added the product
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(choices=CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # update product stock
    def update_stocks(self, items_quantity):
        self.stock -= items_quantity
        self.save()
        

    class Meta:
        indexes = [            
            # Price filtering (range queries)
            models.Index(fields=['price']),
        ]

    def __str__(self):
        return self.name
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/images/")
    alt_text = models.CharField(max_length=64, blank=True)
    is_feature = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    STATUS = (
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
        ("Returned", "Returned"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    order_status= models.CharField(choices=STATUS, null=False, default="pending", max_length=10)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tx_ref = models.CharField(max_length=128, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            # Most frequent: User's order history
            models.Index(fields=["user", "-created_at"], name="user_order_history_idx"),
        ]

    def total_amount(self):
        result = self.items.aggregate(total=Sum(F("price") * F("quantity")))["total"]
        return result or 0.00
    
    def __str__(self):
        return f"Order #{self.id} by {self.user.username} status: {self.order_status}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    # PROTECT prod from deletion if present in past orders
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    price  = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_price(self):
        return self.quantity * self.price

    class Meta:
        indexes = [
            # Frequent: Order details page
            models.Index(fields=['order', 'product']),
        ]

    def __str__(self):
        return f"Order {self.order.id} Item: {self.product.name} x {self.quantity}"


class Payment(models.Model):

    # status of payment
    STATUS = (

        ("cancel", "Cancel"),
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("paid", "Paid"),
        ("failed", "Failed"),
        ("Refunded", "Refunded"),
    )
    
    # payment method
    METHOD = (
        ("card", "Card"),
        ("transfer", "Transfer"),
        ("cash", "Cash")
    )

    # allowed field
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(choices=STATUS, null=False, default="pending", max_length=10)
    tx_ref = models.CharField(null=True, max_length=128)
    method = models.CharField(max_length=16, choices=METHOD, default="card")
    paid_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            # User payment history
            models.Index(fields=['user', 'paid_at']),
        ]
        
    def __str__(self):
        return f"Payment {self.id} user: {self.user.username} for Order {self.order.id} status: {self.status}"
