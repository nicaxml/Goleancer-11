from django.urls import path
from .views import (
    register_view, 
    login_view, 
    dashboard_view,
    landingpage_view, 
    add_to_cart, 
    checkout, 
    update_cart, 
    remove_from_cart,
    user_choices_view, 
    payment_method_view, 
    delete_account_view, 
    update_profile_view, 
    profile_view,

    create_transaction
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', landingpage_view, name='landingpage'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),  # URL untuk halaman dashboard
    path('delete', delete_account_view, name='deleteacc'),
    path('updateprofile', update_profile_view, name='updateprofile'),
    path('profile/', profile_view, name='profile'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('checkout/', checkout, name='checkout'),
    path('update_cart/<int:cart_item_id>/', update_cart, name='update_cart'),
    path('remove_from_cart/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),
    path('payment-method/', payment_method_view, name='payment_method'),
    path('userchoices/', user_choices_view, name='user_choices_form'),
    path('create-transaction/', create_transaction, name='create_transaction'),  # Endpoint untuk membuat transaksi
]

# Tambahkan ini jika Anda menggunakan media/static files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
