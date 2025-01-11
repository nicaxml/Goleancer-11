from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django import forms
from django.contrib.auth.decorators import login_required
import requests
from .models import Product
from .models import Product, Cart , CartItem, Category
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import uuid
from django.conf import settings
from decimal import Decimal
from .forms import UserChoicesForm



#forms.register
class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        }),
        label="Password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        }),
        label="Confirm Password"
    )
#register
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        labels = {
            'username': 'Username',
            'email': 'Email',
            'password': 'Password'
        }
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your password'
            })
        }
#validation
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")

# Register view
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Registrasi berhasil!')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'Goleancer/register.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login berhasil!')
            return redirect('dashboard')  # Sesuaikan URL tujuan setelah login
        else:
            messages.error(request, 'Username atau password salah')
    return render(request, 'Goleancer/login.html')

#landingpage view
def landingpage_view(request):
    return render(request, 'Goleancer/landingpage.html')  

#dashboard view
@login_required
def dashboard_view(request):
    # Ambil query parameter
    search_query = request.GET.get('search', '')
    category_id = request.GET.get('category', '')

    # Ambil semua produk
    products = Product.objects.all()

    # Filter berdasarkan pencarian
    if search_query:
        products = products.filter(name__icontains=search_query)

    # Filter berdasarkan kategori
    if category_id:
        products = products.filter(category_id=category_id)

    # Ambil semua kategori untuk dropdown
    categories = Category.objects.all()

    context = {
        'products': products,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_id,
    }
    return render(request, 'Goleancer/dashboard.html', context)



############
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1  # Tambahkan jumlah jika sudah ada
        cart_item.save()
    messages.success(request, f"{product.name} berhasil ditambahkan ke keranjang!")
    return redirect('checkout')  # Arahkan ke dashboard atau halaman lain sesuai kebutuhan


@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all()  # Ambil semua item di keranjang
    total_price = sum(item.subtotal() for item in cart_items)  # Hitung total harga
    return render(request, 'Goleancer/checkout.html', {'cart_items': cart_items, 'total_price': total_price})


@login_required
def update_cart(request, item_id):
    if request.method == "POST":
        action = request.POST.get("action")
        cart_item = get_object_or_404(CartItem, id=item_id)
        if action == "increase":
            cart_item.quantity += 1
        elif action == "decrease" and cart_item.quantity > 1:
            cart_item.quantity -= 1
        cart_item.save()
    return redirect('checkout')  # Adjust as needed

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    if request.method == 'POST':
        cart_item.delete()
    return redirect('checkout')


@login_required
def payment_method_view(request):
    if request.method == 'POST':
        selected_payment_method = request.POST.get('payment_method')
        if selected_payment_method:
            messages.success(request, f"Metode pembayaran '{selected_payment_method}' dipilih!")
            return redirect('checkout')  # Replace with the next step, e.g., 'payment_summary'

    payment_methods = ['Credit Card', 'Bank Transfer', 'E-Wallet']
    return render(request, 'Goleancer/payment_method.html', {'payment_methods': payment_methods})

@login_required
def delete_account_view(request):
    if request.method == 'POST':  # Hanya izinkan POST request untuk keamanan
        user = request.user
        user_email = user.email
        user.delete()
        messages.success(request, f"Akun dengan email {user_email} telah dihapus.")
        return redirect('https://accounts.google.com/Logout') # Arahkan ke halaman setelah penghapusan akun
    return render(request, 'Goleancer/deleteacc.html') 

@login_required
def profile_view(request):
    return render(request, 'Goleancer/profile.html')

@login_required
def update_profile_view(request):
    if request.method == 'POST':
        # Proses form untuk memperbarui data pengguna
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST.get('password')

        user = request.user
        user.username = username
        user.email = email

        if password:
            user.set_password(password)  # Update password jika ada perubahan
        user.save()

        messages.success(request, 'Profil berhasil diperbarui!')
        return redirect('profile')  # Kembali ke halaman profil setelah update

    return render(request, 'Goleancer/update_profile.html')
@login_required
def create_transaction(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all()
    total_price = float(sum(item.subtotal() for item in cart_items))  # Convert to float

    if total_price == 0:
        messages.error(request, "Keranjang kosong. Tambahkan produk terlebih dahulu.")
        return redirect('dashboard')

    order_id = str(uuid.uuid4())
    transaction_data = {
        "transaction_details": {
            "order_id": order_id,
            "gross_amount": total_price,  # Ensure this is a float
        },
        "customer_details": {
            "first_name": request.user.username,
            "email": request.user.email,
        },
        "item_details": [
            {
                "id": item.product.id,
                "price": float(item.product.price),  # Convert to float
                "quantity": item.quantity,
                "name": item.product.name
            } for item in cart_items
        ],
    }

    url = settings.MIDTRANS_BASE_URL + "charge"
    headers = {
        "Authorization": "Basic " + settings.MIDTRANS_SERVER_KEY,
        "Content-Type": "application/json",
    }

    response = requests.post(url, json=transaction_data, headers=headers)

    if response.status_code == 200:
        payment_url = response.json().get('redirect_url')
        return redirect(payment_url)
    else:
        messages.error(request, "Gagal membuat transaksi.")
        return redirect('checkout')
    

def user_choices_view(request):
    if request.method == 'POST':
        form = UserChoicesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('user_choices_form')  # Ganti 'success' dengan nama URL yang sesuai
    else:
        form = UserChoicesForm()
    return render(request, 'Goleancer/user_choices_form.html', {'form': form})
