
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework.permissions import AllowAny
from .models import Product, Review, Order
from .serializers import ProductSerializer, ReviewSerializer, OrderSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout

from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.core.mail import send_mail
from django.conf import settings





from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta
from rest_framework.permissions import IsAdminUser
from django.contrib.auth import get_user_model



class AdminDashboardAPI(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        User = get_user_model()
        now = timezone.now()

        last_week = now - timedelta(days=7)
        last_month = now - timedelta(days=30)

        orders_last_week = Order.objects.filter(created_at__gte=last_week).count()
        orders_last_month = Order.objects.filter(created_at__gte=last_month).count()

        top_products = Product.objects.annotate(
            likes=Count("wishlisted_by")
        ).order_by("-likes")[:5]

        top_users = User.objects.annotate(
            total_orders=Count("order")
        ).order_by("-total_orders")[:5]

        current_month_sales = Order.objects.filter(
            created_at__month=now.month
        ).aggregate(total=Sum("total_amount"))

        previous_month_sales = Order.objects.filter(
            created_at__month=now.month - 1
        ).aggregate(total=Sum("total_amount"))

        return Response({
            "orders_last_week": orders_last_week,
            "orders_last_month": orders_last_month,
            "most_liked_products": [p.name for p in top_products],
            "top_buyers": [u.username for u in top_users],
            "current_month_sales": current_month_sales["total"],
            "previous_month_sales": previous_month_sales["total"],
        })






class ProductListAPI(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()

        size = self.request.query_params.get("size")
        color = self.request.query_params.get("color")
        sort = self.request.query_params.get("sort")

        if size:
            queryset = queryset.filter(size=size)

        if color:
            queryset = queryset.filter(color__iexact=color)

        if sort == "price_low":
            queryset = queryset.order_by("price")

        if sort == "price_high":
            queryset = queryset.order_by("-price")

        return queryset


class ProductDetailAPI(generics.RetrieveAPIView):
    """
    Returns single product
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ReviewCreateAPI(generics.CreateAPIView):
    """
    Create a product review
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]


class OrderCreateAPI(generics.CreateAPIView):
    """
    Create an order
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        order = serializer.save(user=self.request.user)

        send_mail(
            "Order Confirmation",
            f"Your order #{order.id} has been successfully placed.",
            settings.EMAIL_HOST_USER,
            [self.request.user.email],
            fail_silently=True,
        )


class OrderListAPI(generics.ListAPIView):
    """
    Show logged in user's orders
    """
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class ProductReviewsAPI(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Review.objects.none()

        product_id = self.kwargs.get("pk")
        return Review.objects.filter(product_id=product_id)


class RegisterAPI(APIView):
    """
    Register a new user and send email activation link
    """

    def post(self, request):
        User = get_user_model()

        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")

        if not username or not email or not password:
            return Response({"error": "Missing fields"}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=400)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_active=False
        )

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        activation_link = f"{request.scheme}://{request.get_host()}/api/activate/{uid}/{token}/"

        send_mail(
            "Activate your Dhaka Threads account",
            f"Click this link to activate your account:\n{activation_link}",
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=True
        )

        return Response(
            {"message": "User registered. Check email to activate account."},
            status=status.HTTP_201_CREATED
        )    
    
class LoginAPI(APIView):
    """
    Login user
    """

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user is None:
            return Response({"error": "Invalid credentials"}, status=400)

        if not user.is_active:
            return Response({"error": "Account not activated"}, status=403)

        login(request, user)

        return Response({"message": "Login successful"}) 



class LogoutAPI(APIView):
    """
    Logout user
    """

    def post(self, request):
        logout(request)
        return Response({"message": "Logged out"})
    



class ActivateAccountAPI(APIView):
    """
    Activate account via email link
    """

    def get(self, request, uidb64, token):
        User = get_user_model()

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception:
            user = None

        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"message": "Account activated successfully"})
        else:
            return Response({"error": "Invalid activation link"}, status=400)




from .models import Wishlist
from .serializers import WishlistSerializer


class WishlistAPI(generics.ListCreateAPIView):
    serializer_class = WishlistSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RelatedProductsAPI(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Product.objects.none()

        product_id = self.kwargs.get("pk")
        product = Product.objects.get(pk=product_id)

        return Product.objects.filter(
            category=product.category
        ).exclude(id=product_id)[:5]

import requests
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["POST"])
def create_payment(request):

    order_id = request.data.get("order_id")
    total_amount = request.data.get("total_amount")

    tran_id = f"ORDER_{order_id}"

    data = {
        "store_id": settings.SSLCOMMERZ_STORE_ID,
        "store_passwd": settings.SSLCOMMERZ_STORE_PASS,

        "total_amount": total_amount,
        "currency": "BDT",

        "tran_id": tran_id,

        "success_url": "https://final-exam-delta-two.vercel.app/api/payment/success/",
        "fail_url": "https://final-exam-delta-two.vercel.app/api/payment/fail/",
        "cancel_url": "https://final-exam-delta-two.vercel.app/api/payment/cancel/",

        "cus_name": "Customer",
        "cus_email": "customer@email.com",
        "cus_phone": "01700000000",

        "product_name": "Dhaka Threads Order",
        "product_category": "Clothing",
        "product_profile": "general",

        "shipping_method": "NO",
        "num_of_item": 1,
    }

    response = requests.post(
        "https://sandbox.sslcommerz.com/gwprocess/v4/api.php",
        data=data
    )

    payment_data = response.json()

    return Response({
        "gateway_url": payment_data["GatewayPageURL"]
    })

@api_view(["POST"])
def payment_success(request):

    tran_id = request.data.get("tran_id")

    try:
        order_id = tran_id.split("_")[1]

        from .models import Order
        order = Order.objects.get(id=order_id)

        order.status = "PAID"
        order.save()

    except Exception as e:
        return Response({"error": str(e)})

    return Response({"message": "Payment successful"})


@api_view(["POST"])
def payment_fail(request):
    return Response({"message": "Payment failed"})

@api_view(["POST"])
def payment_cancel(request):
    return Response({"message": "Payment cancelled"})    