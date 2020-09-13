from django.contrib.auth.models import AbstractUser
from django.db import models
import django.utils.timezone


class User(AbstractUser):
    bio = models.TextField(blank=True, max_length=100)
    profile_photo = models.ImageField(upload_to='media/%Y/%m/%d/', default=None, null=True, blank=True)
    header_photo = models.ImageField(upload_to="media/%Y/%m/%d/", default=None, null=True, blank=True)
    is_verified = models.BooleanField(default=False)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator")
    content = models.TextField(blank=False, max_length=280)
    likes = models.IntegerField(default=0)
    posted_date = models.DateTimeField(default=django.utils.timezone.now)

    def __str__(self):
        return f"{self.user}, {self.content}"


class Follow(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    following = models.ManyToManyField(User, related_name="following", blank=True)
    followers = models.ManyToManyField(User, related_name="followers", blank=True)

    def __str__(self):
        return f"{self.user}"


class Like(models.Model):
    post = models.IntegerField(default=0)
    user = models.ManyToManyField(User, blank=True, related_name="user_like")

    def __str__(self):
        return f"POST_ID: {self.post}"