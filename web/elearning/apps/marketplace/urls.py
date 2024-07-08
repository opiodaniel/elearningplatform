from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (home, seller_dashboard, public_product_list, product_list, add_to_cart, view_cart, remove_from_cart,
                    checkout, product_detail, order_history, product_search, update_user_profile, profile,
                    delete_user_account, add_product, edit_product, delete_product, leave_review, SignUpView)


urlpatterns = [
    path('', home, name='home'),
    path('seller_dashboard/', seller_dashboard, name='seller_dashboard'),
    path('public_product_list/', public_product_list, name='public_product_list'),
    path('product_list/', product_list, name='product_list'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('view_cart/', view_cart, name='view_cart'),
    path('remove_from_cart/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),
    path('checkout/', checkout, name='checkout'),
    path('leave_review/<int:product_id>/', leave_review, name='leave_review'),  # Updated URL
    path('product_detail/<int:product_id>/', product_detail, name='product_detail'),
    path('order_history/', order_history, name='order_history'),
    path('product_search/', product_search, name='product_search'),
    path('update_user_profile/', update_user_profile, name='update_user_profile'),
    path('delete_user_account/', delete_user_account, name='delete_user_account'),
    path('add_product/', add_product, name='add_product'),
    path('edit_product/<int:product_id>/', edit_product, name='edit_product'),
    path('delete_product/<int:product_id>/', delete_product, name='delete_product'),
    path(r'signup/', SignUpView.as_view(), name='signup'),
    # path('signup/', auth_views.SignupView.as_view(), name='signup'),
    # path( r'^login/$',auth_views.LoginView.as_view(template_name="useraccounts/login.html"), name="login"),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('account/profile/', profile, name='profile'),
    # Add other paths as needed
]
