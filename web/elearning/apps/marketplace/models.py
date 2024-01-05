from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from ckeditor_uploader.fields import RichTextUploadingField


class UserProfile(models.Model):
    class Meta:
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    is_seller = models.BooleanField(default=False)
    short_bio = RichTextUploadingField(blank=True, null=True)
    bio = RichTextUploadingField(blank=True, null=True)
    #
    address = models.CharField(max_length=128, default='', blank=True)
    zip = models.CharField(max_length=20, default='', blank=True)
    city = models.CharField(max_length=100, default='', blank=True)
    country = models.CharField(max_length=100, default='', blank=True)
    #
    phone = models.CharField(max_length=20, default='', blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name()
    # Add additional fields as needed (e.g., profile picture, contact information)


class Product(models.Model):
    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_available = models.PositiveIntegerField(default=0)
    is_public = models.BooleanField(default=False)


class Order(models.Model):
    buyer = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    item_price = models.DecimalField(max_digits=10, decimal_places=2)


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField('Product', through='CartItem')


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)


class Review(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

