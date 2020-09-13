from django.contrib.auth.models import AbstractUser
from django.db import models
import django.utils.timezone



class User(AbstractUser):
    pass


class Auction_listings(models.Model):
    CATEGORY_CHOICES = [
        ("Art", "Art"),
        ("Books", "Books"),
        ("Cars", "Cars"),
        ("Clothes", "Clothes"),
        ("Games", "Games"),
        ("Health & Beauty", "Health & Beauty"),
        ("Home", "Home"),
        ("Literature", "Literature"),
        ("Music", "Music"),
        ("Puzzle", "Puzzle"),
        ("Science", "Science"),
        ("Sports", "Sports"),
        ("Technology", "Technology"),
        ("Toys", "Toys"),
        ("Others", "Others")
    ]

    product_image = models.CharField(max_length=500)
    product_title = models.CharField(max_length=40)
    product_description = models.CharField(max_length=1000)
    product_category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default="Others")
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_closed = models.BooleanField(default=False)
    winner = models.ForeignKey(User, default=None, blank=True, null=True, on_delete=models.CASCADE, related_name="winner")
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    post_date = models.DateTimeField(default=django.utils.timezone.now)
 
    def __str__(self):
        return f"{self.product_title}"


class Bid(models.Model):
    auction_name = models.ForeignKey(Auction_listings, on_delete=models.CASCADE)
    username = models.CharField(max_length=64)
    bid_value = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.bid_value} by {self.username} in {self.auction_name}"



class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Auction_listings, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.item}, in {self.user}'s watchlist"


class Comments(models.Model):
    auction = models.ForeignKey(Auction_listings, on_delete=models.CASCADE)
    username = models.CharField(max_length=64)
    content = models.CharField(max_length=350)
    date = models.DateTimeField(default=django.utils.timezone.now)

    def __str__(self):
        return f"by {self.username} in {self.auction} in {self.date}"