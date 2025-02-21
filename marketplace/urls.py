from django.urls import path
from . import views

urlpatterns = [
    # Vendor URLs
    path('vendors/', views.vendor_list, name='vendor_list'),
    path('vendor/<int:vendor_id>/', views.vendor_details, name='vendor_details'),

    # Product URLs
    path('products/', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_details, name='product_details'),

    # Cart URLs (Fixed Duplicates)
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/update/<int:cart_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),

    # Order URLs
    path('orders/', views.order_list, name='order_list'),

    # Checkout URL
    path('checkout/', views.checkout, name='checkout'),

    # Authentication URLs (Fixed Register Path)
    path('', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
