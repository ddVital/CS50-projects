from django.contrib import admin
from .models import Auction_listings, Bid, Comments, User, Watchlist


# Register your models here.
admin.site.register(Auction_listings)
admin.site.register(Bid)
admin.site.register(Comments)
admin.site.register(User)
admin.site.register(Watchlist)