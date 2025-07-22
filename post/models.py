from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'category'

    def __str__(self):
        return self.name

class Laptop(models.Model):
    brand = models.CharField(max_length=100)
    cpu = models.CharField(max_length=10)
    gpu = models.CharField(max_length=15)
    ram = models.CharField(max_length=15)
    storage = models.IntegerField()
    manitor = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='news_images/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:        
        db_table = 'Laptop'




    def __str__(self):
        return self.brand
    



class Contact(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)


    class Meta:
        db_table = 'contact'



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gmail = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    rasm = models.ImageField(upload_to='news_images/', blank=True, null=True)


class Comment(models.Model):
    laptop = models.ForeignKey(Laptop, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.text[:30]}"