from rest_framework import serializers
from .models import User, Product, Category, Review, Order, OrderItem


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


from django.db.models import Avg

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = "__all__"

    def get_average_rating(self, obj):
        return obj.reviews.aggregate(avg=Avg("rating"))["avg"]


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"

        
from .models import Wishlist


class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = "__all__"
