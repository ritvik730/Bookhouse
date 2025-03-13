from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
# Create your models here.


class Contact(models.Model):
    name = models.CharField(max_length=50, default="name")
    email = models.EmailField(max_length=50, default="email")
    phone = models.IntegerField(default="0")
    message = models.TextField()

    def __str__(self):
        return self.email


class Profile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class ResetProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    forget_password_token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user


class Category(models.Model):
    category_name = models.CharField(max_length=100)
    # category_image = models.ImageField(upload_to="cat_images/", default="")

    def __str__(self):
        return self.category_name



class Status(models.Model):
    status = models.CharField(max_length=50, default=1)

    def __str__(self):
        return self.status

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    product_title = models.CharField(max_length=100)
    prod_desc = models.TextField(max_length=1000)
    price = models.IntegerField()
    pub_date = models.DateField()
    product_image = models.ImageField(upload_to='product_images/', default="")


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default='Your Name')
    bio = models.CharField(max_length=200, default='Your Bio')
    phone = models.CharField(max_length=20, default="0000000000")
    address = models.CharField(max_length=200, default='Your address')
    photo = models.ImageField(
        upload_to='profile_image/', default='image/user.png')

class Wishlist(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    desc = models.CharField(max_length=50, default='wishlist')

