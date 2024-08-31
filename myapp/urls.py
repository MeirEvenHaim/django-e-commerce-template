from django.urls import path
from myapp.views.cart_itemViews import cart_item_detail, cart_item_list
from myapp.views.categoryViews import category_detail, category_list_create
from myapp.views.payment import payment_detail, payment_list
from myapp.views.productViews import product_detail, product_list
from myapp.views.registerViews import register
from myapp.views.shipping import shipping_detail, shipping_list
from myapp.views.supplierViews import supplier_detail, supplier_list
from myapp.views.userView import UserViewSet
from myapp.views.loginView import CustomTokenObtainPairView
from myapp.views.orders import order_detail, order_list
from myapp.views.cartViews import cart_detail, cart_list

# User view set
user_list = UserViewSet.as_view({
    'get': 'list',    # Admins can list all users
    'post': 'update', # Update user (if needed)
    'delete': 'destroy' # Admins can delete users
})

user_detail = UserViewSet.as_view({
    'get': 'retrieve',  # Users can view their own profile
    'put': 'update',    # Users can update their own profile
})

urlpatterns = [
    # Authentication and registration URLs
    path('register/', register, name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),

    # User management URLs
    path('users/', user_list, name='user-list'),  # Admins can list all users
    path('users/<int:pk>/', user_detail, name='user-detail'),  # Users can view/update their own profile

    # Category URLs
    path('categories/', category_list_create, name='category-list'),
    path('categories/<int:pk>/', category_detail, name='category-detail'),
    
    # Supplier URLs
    path('suppliers/', supplier_list, name='supplier-list'),
    path('suppliers/<int:pk>/', supplier_detail, name='supplier-detail'),
    
    # Product URLs
    path('products/', product_list, name='product-list'),
    path('products/<int:pk>/', product_detail, name='product-detail'),
    
    # Cart URLs
    path('carts/', cart_list, name='cart-list'),
    path('carts/<int:pk>/', cart_detail, name='cart-detail'),
    
    # CartItem URLs
    path('cart-items/', cart_item_list, name='cart-item-list'),
    path('cart-items/<int:pk>/', cart_item_detail, name='cart-item-detail'),
    
    # Order URLs
    path('orders/', order_list, name='order-list'),
    path('orders/<int:pk>/', order_detail, name='order-detail'),
    
    # Payment URLs
    path('payments/', payment_list, name='payment-list'),
    path('payments/<int:pk>/', payment_detail, name='payment-detail'),
    
    # Shipping URLs
    path('shippings/', shipping_list, name='shipping-list'),
    path('shippings/<int:pk>/', shipping_detail, name='shipping-detail'),
]
