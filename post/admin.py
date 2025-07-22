from django.contrib import admin
from .models import Category, Laptop, Contact, Profile, Comment
# Register your models here.

class LaptopAdmin(admin.ModelAdmin):
    list_display = ('brand', 'created_at', 'author', 'ram')
    search_fields = ('brand', 'price')  
    list_filter = ('created_at', 'ram')

admin.site.register(Category)
admin.site.register(Laptop, LaptopAdmin)   
admin.site.register(Contact)
admin.site.register(Profile)
admin.site.register(Comment)