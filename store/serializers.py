from rest_framework import serializers
from django.db.models import Avg
from .models import User, Product, Category, Review, Order, OrderItem

from django.contrib.auth.models import User
from rest_framework import serializers




class UserSerializer(serializers.ModelSerializer):
    # Explicitly defining these prevents the 'NoneType' meta error
    username = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"



class ProductSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__' # Or list your specific fields

    def get_average_rating(self, obj):
        # This looks at all related reviews and calculates the average 'rating'
        average = obj.reviews.aggregate(Avg('rating'))['rating__avg']
        return round(average, 1) if average else 0

    def get_review_count(self, obj):
        return obj.reviews.count()


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"

class OrderItemSerializer(serializers.ModelSerializer):
    # Use an explicit PrimaryKeyRelatedField to bypass hidden validation issues
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

# serializers.py

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Order
        
        fields = ['id', 'user', 'total_amount', 'address', 'full_name', 'items', 'status', 'created_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        order = Order.objects.create(**validated_data)
        
        for item_data in items_data:
            # item_data['product'] is the Product object because of the Serializer validation
            product = item_data['product']
            
            # THE FIX: Manually assign the price from the product to the order item
            OrderItem.objects.create(
                order=order, 
                product=product,
                quantity=item_data['quantity'],
                price=product.price  # Grabbing the current price of the product
            )
            
        return order
      
from .models import Wishlist


class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = "__all__"
