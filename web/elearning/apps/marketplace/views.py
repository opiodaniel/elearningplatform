from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from .models import UserProfile, Product, Cart, CartItem, Order, OrderItem, Review
from .forms import UserProfileForm, ProductForm, ReviewForm
from django.db.models import Avg
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views import generic


def home(request):
    # Fetch some featured products for the home page
    featured_products = Product.objects.all()[:3]
    return render(request, 'marketplace/home.html', {'featured_products': featured_products})


@login_required
def seller_dashboard(request):
    seller_profile = request.user.userprofile
    seller_products = Product.objects.filter(seller=seller_profile)
    return render(request, 'marketplace/seller_dashboard.html', {'seller_profile': seller_profile, 'seller_products': seller_products})


def public_product_list(request):
    public_products = Product.objects.filter(is_public=True)
    return render(request, 'marketplace/public_product_list.html', {'public_products': public_products})


def product_list(request):
    products = Product.objects.all()
    return render(request, 'marketplace/product_list.html', {'products': products})


@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    user_cart, created = Cart.objects.get_or_create(user=request.user)

    # Check if the product is already in the cart, update quantity
    cart_item, created = CartItem.objects.get_or_create(cart=user_cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('view_cart')


@login_required
def view_cart(request):
    user_cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = user_cart.cartitem_set.all()
    total_amount = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'marketplace/view_cart.html', {'cart_items': cart_items, 'total_amount': total_amount})


@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = CartItem.objects.get(pk=cart_item_id)
    cart_item.delete()
    return redirect('view_cart')


@login_required
def checkout(request):
    user_cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = user_cart.cartitem_set.all()
    total_amount = sum(item.product.price * item.quantity for item in cart_items)

    # Create an order
    order = Order.objects.create(user=request.user, total_amount=total_amount)

    # Create order items
    for cart_item in cart_items:
        OrderItem.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity, item_price=cart_item.product.price)

    # Clear the cart
    user_cart.cartitem_set.all().delete()

    return render(request, 'marketplace/order_confirmation.html', {'order': order})


@login_required
def leave_review(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        rating = int(request.POST['rating'])
        comment = request.POST['comment']

        # Create a review
        Review.objects.create(product=product, user=request.user, rating=rating, comment=comment)

    return redirect('product_detail', product_id=product_id)


@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product)
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    # average_rating = reviews.aggregate(models.Avg('rating'))['rating__avg']

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('product_detail', product_id=product.id)  # Redirect to product detail page after leaving review
    else:
        form = ReviewForm()

    return render(request, 'marketplace/product_detail.html', {'product': product, 'reviews': reviews,
                                                                                    'form': form,'average_rating': average_rating})


# @login_required
# def order_history(request):
#     user_orders = Order.objects.filter(user=request.user)
#
#     return render(request, 'marketplace/order_history.html', {'user_orders': user_orders})

@login_required
def order_history(request):
    user_profile = UserProfile.objects.get(user=request.user)
    orders = Order.objects.filter(user=user_profile).order_by('-created_at')

    return render(request, 'marketplace/order_history.html', {'orders': orders})

# @login_required
# def product_search(request):
#     query = request.GET.get('q')
#     if query:
#         search_results = Product.objects.filter(name__icontains=query, is_public=True)
#     else:
#         search_results = None
#
#     return render(request, 'marketplace/product_search.html', {'query': query, 'search_results': search_results})

@login_required
def product_search(request):
    query = request.GET.get('q')

    if query:
        results = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    else:
        results = []

    return render(request, 'marketplace/product_search.html', {'query': query, 'results': results})


@login_required
def update_user_profile(request):
    user_profile = request.user.userprofile

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('seller_dashboard')  # Redirect to seller dashboard after profile update
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'marketplace/update_user_profile.html', {'form': form})


# @login_required
# def update_user_profile(request):
#     user_profile = UserProfile.objects.get(user=request.user)
#
#     if request.method == 'POST':
#         form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
#         if form.is_valid():
#             form.save()
#             return redirect('home')  # Redirect to home page after updating profile
#     else:
#         form = UserProfileForm(instance=user_profile)
#
#     return render(request, 'marketplace/update_user_profile.html', {'form': form})

#
# @login_required
# def delete_user_account(request):
#     if request.method == 'POST':
#         user = request.user
#         user.delete()
#         messages.success(request, 'Your account has been deleted successfully.')
#         return redirect('home')  # Redirect to your home page
#
#     return render(request, 'marketplace/delete_user_account.html')
@login_required
def delete_user_account(request):
    user = request.user

    if request.method == 'POST':
        user.delete()
        logout(request)
        messages.success(request, 'Your account has been deleted.')
        return redirect('home')  # Redirect to home page after deleting account

    return render(request, 'marketplace/delete_user_account.html', {'user': user})


@login_required
def add_product(request):
    if not request.user.userprofile.is_seller:
        return redirect('home')  # Redirect non-sellers to home

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user.userprofile
            product.save()
            return redirect('seller_dashboard')  # Redirect to seller dashboard after adding product
    else:
        form = ProductForm()

    return render(request, 'marketplace/add_product.html', {'form': form})

# @login_required
# def add_product(request):
#     if request.method == 'POST':
#         form = ProductForm(request.POST)
#         if form.is_valid():
#             product = form.save(commit=False)
#             product.seller = request.user.userprofile
#             product.save()
#             return redirect('seller_dashboard')  # Redirect to seller dashboard after adding product
#     else:
#         form = ProductForm()
#
#     return render(request, 'marketplace/add_product.html', {'form': form})


# @login_required
# def edit_product(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#
#     if request.user.userprofile != product.seller:
#         return redirect('home')  # Redirect users who are not the seller of the product
#
#     if request.method == 'POST':
#         form = ProductForm(request.POST, instance=product)
#         if form.is_valid():
#             form.save()
#             return redirect('seller_dashboard')  # Redirect to seller dashboard after editing product
#     else:
#         form = ProductForm(instance=product)
#
#     return render(request, 'marketplace/edit_product.html', {'form': form, 'product': product})

@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Ensure that only the seller who created the product can edit it
    if request.user != product.seller.user:
        return redirect('seller_dashboard')

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('seller_dashboard')  # Redirect to seller dashboard after editing product
    else:
        form = ProductForm(instance=product)

    return render(request, 'marketplace/edit_product.html', {'form': form, 'product': product})


# @login_required
# def delete_product(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#
#     if request.user.userprofile != product.seller:
#         return redirect('home')  # Redirect users who are not the seller of the product
#
#     if request.method == 'POST':
#         product.delete()
#         return redirect('seller_dashboard')  # Redirect to seller dashboard after deleting product
#
#     return render(request, 'marketplace/delete_product.html', {'product': product})


@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Ensure that only the seller who created the product can delete it
    if request.user != product.seller.user:
        return redirect('seller_dashboard')

    if request.method == 'POST':
        product.delete()
        return redirect('seller_dashboard')  # Redirect to seller dashboard after deleting product

    return render(request, 'marketplace/delete_product.html', {'product': product})


@login_required
def leave_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('product_detail', product_id=product.id)  # Redirect to product detail page after leaving review
    else:
        form = ReviewForm()

    return render(request, 'marketplace/leave_review.html', {'form': form, 'product': product})


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    model = User
    template_name = 'marketplace/signup.html'


@login_required
def profile(request):
    # Add any logic needed for the profile view
    return render(request, 'account/profile.html')