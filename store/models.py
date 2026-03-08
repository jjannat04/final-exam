from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# 1. CUSTOM USER
class User(AbstractUser):
    is_customer = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, blank=True)

# 2. CATEGORY & PRODUCT
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Categories"
    

    def __str__(self): 
        return self.name


class Product(models.Model):
    SIZE_CHOICES = [('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('XL', 'Extra Large')]
    COLOR_CHOICES = [('Red', 'Red'), ('Blue', 'Blue'), ('Black', 'Black'), ('White', 'White')]
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='products/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=2, choices=SIZE_CHOICES)
    color = models.CharField(max_length=20, choices=COLOR_CHOICES)
    description = models.TextField()
    stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): return self.name

# 3. ORDER & WISHLIST

class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    address = models.TextField()
    city = models.CharField(max_length=100, default="Dhaka")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

class Wishlist(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wishlist"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="wishlisted_by"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "product"]

    def __str__(self):
        return f"{self.user} -> {self.product}"

# 4. REVIEW
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)]) # 1 to 5 stars
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating} Stars)"
    



