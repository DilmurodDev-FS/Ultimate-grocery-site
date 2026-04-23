from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from .forms import CheckoutForm, RegisterForm, ProfileForm
from .models import Category, Product, Order, OrderItem, UserProfile
from .telegram_utils import send_order_to_telegram

def home(request):
    products = Product.objects.filter(is_active=True).select_related('category')
    q = request.GET.get('q', '')
    category_filter = request.GET.get('category', 'all')

    if q:
        products = products.filter(
            Q(name__icontains=q) |
            Q(short_description__icontains=q) |
            Q(description__icontains=q)
        )

    if category_filter != 'all':
        products = products.filter(product_type=category_filter)

    return render(request, 'store/home.html', {
        'products': products,
        'featured_products': Product.objects.filter(is_active=True, is_featured=True)[:4],
        'categories': Category.objects.all(),
        'search_query': q,
        'current_category': category_filter,
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related_products = Product.objects.filter(category=product.category, is_active=True).exclude(id=product.id)[:4]
    return render(request, 'store/product_detail.html', {'product': product, 'related_products': related_products})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart = request.session.get('cart', {})
    key = str(product.id)
    if key in cart:
        cart[key]['qty'] += 1
    else:
        cart[key] = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'emoji': product.image_emoji,
            'qty': 1,
        }
    request.session['cart'] = cart
    request.session.modified = True
    messages.success(request, f"{product.name} savatchaga qo'shildi.")
    return redirect(request.META.get('HTTP_REFERER', 'home'))

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    key = str(product_id)
    if key in cart:
        del cart[key]
        request.session['cart'] = cart
        request.session.modified = True
        messages.info(request, "Mahsulot savatchadan olib tashlandi.")
    return redirect('cart')

def cart_view(request):
    cart = request.session.get('cart', {})
    items = list(cart.values())
    total = sum(item['price'] * item['qty'] for item in items)
    return render(request, 'store/cart.html', {'cart_items': items, 'total': total})

def checkout(request):
    cart = request.session.get('cart', {})
    items = list(cart.values())
    if not items:
        messages.warning(request, "Savatchangiz bo'sh.")
        return redirect('home')

    total = sum(item['price'] * item['qty'] for item in items)

    initial = {}
    if request.user.is_authenticated:
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        initial = {
            'full_name': request.user.get_full_name() or request.user.username,
            'phone': profile.phone,
            'address': profile.address,
        }

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                full_name=form.cleaned_data['full_name'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
                notes=form.cleaned_data['notes'],
                payment_method=form.cleaned_data['payment_method'],
                total_price=total,
                payment_status='pending',
            )

            for item in items:
                OrderItem.objects.create(
                    order=order,
                    product_name=item['name'],
                    price=item['price'],
                    quantity=item['qty'],
                )

            if request.user.is_authenticated:
                profile, _ = UserProfile.objects.get_or_create(user=request.user)
                profile.phone = form.cleaned_data['phone']
                profile.address = form.cleaned_data['address']
                profile.save()

            send_order_to_telegram(order)

            request.session['cart'] = {}
            request.session.modified = True

            if order.payment_method in ('click', 'payme'):
                messages.info(request, "To'lov tizimi uchun merchant ma'lumotlarini qo'yganingizdan keyin real integratsiya ishlaydi. Hozircha buyurtma saqlandi.")
                return redirect('payment_info')

            messages.success(request, "Buyurtma muvaffaqiyatli qabul qilindi.")
            return redirect('order_success', order_id=order.id)
    else:
        form = CheckoutForm(initial=initial)

    return render(request, 'store/checkout.html', {'form': form, 'cart_items': items, 'total': total})

def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'store/order_success.html', {'order': order})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.email = form.cleaned_data['email']
            user.first_name = form.cleaned_data['first_name']
            user.save()
            UserProfile.objects.get_or_create(user=user)
            login(request, user)
            messages.success(request, "Akkaunt yaratildi.")
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'store/register.html', {'form': form})

@login_required
def dashboard_view(request):
    orders = request.user.orders.all() if hasattr(request.user, 'orders') else []
    return render(request, 'store/dashboard.html', {'orders': orders})

@login_required
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil yangilandi.")
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'store/profile.html', {'form': form})

def payment_info(request):
    return render(request, 'store/payment_info.html')
