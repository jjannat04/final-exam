from django.urls import path
from . import api_views
from .api_views import (
    ProductListAPI,
    ProductDetailAPI,
    ReviewCreateAPI,
    OrderCreateAPI,
    OrderListAPI,
    ProductReviewsAPI,
    RegisterAPI, LoginAPI, LogoutAPI, ActivateAccountAPI, WishlistAPI, RelatedProductsAPI, AdminDashboardAPI
)

urlpatterns = [
    path("admin-dashboard/", AdminDashboardAPI.as_view(), name="admin-dashboard"),

    path("products/", ProductListAPI.as_view(), name="product-list"),
    path("products/<int:pk>/", ProductDetailAPI.as_view(), name="product-detail"),
    path("reviews/", ReviewCreateAPI.as_view(), name="create-review"),
    path("orders/", OrderListAPI.as_view(), name="order-list"),
    path("orders/create/", OrderCreateAPI.as_view(), name="create-order"),
    path("products/<int:pk>/reviews/", ProductReviewsAPI.as_view(), name="product-reviews"),
    

    path("register/", RegisterAPI.as_view(), name="register"),
    path("login/", LoginAPI.as_view(), name="login"),
    path("logout/", LogoutAPI.as_view(), name="logout"),
    path("activate/<uidb64>/<token>/", ActivateAccountAPI.as_view(), name="activate"),

    path("wishlist/", WishlistAPI.as_view(), name="wishlist"),

    path("products/<int:pk>/related/",RelatedProductsAPI.as_view(),name="related-products"),

    path("create-payment/", api_views.create_payment),
    path("payment/success/", api_views.payment_success),
    path("payment/fail/", api_views.payment_fail),
    path("payment/cancel/", api_views.payment_cancel),

]