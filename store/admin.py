from django.contrib import admin
from .models import User, Category, Product, Order, Review, Wishlist, OrderItem


admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Wishlist)

