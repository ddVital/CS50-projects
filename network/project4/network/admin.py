from django.contrib import admin
from .models import Follow, Post, User

# Register your models here.
admin.site.register(Follow)
admin.site.register(Post)
admin.site.register(User)