import markdown2

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .models import Auction_listings, Bid, Comments, User, Watchlist


def index(request):
    return render(request, "auctions/index.html", {
        "auctions": Auction_listings.objects.all(),
        "bid": Bid.objects.all(),
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create_listing(request):
    username = request.user.username

    # add the auction details
    if request.method == "POST":
        product_img = request.POST.get("product-img")
        title = request.POST.get("title")
        description = request.POST.get("description")
        product_price = request.POST.get("price")
        category = request.POST.get("category")

        new_auction = Auction_listings(product_image=product_img, 
            product_title=title, product_description=description,
            product_category=category, product_price=product_price,
            username=User.objects.get(username=username)
        )

        new_auction.save()

        return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/create.html")


# user informations page
@login_required
def user_page(request, username):
    return render(request, "auctions/profile.html", {
        "user": User.objects.get(username=username),
        "username": request.user.username,
        "won": Auction_listings.objects.filter(winner=request.user)
    })
    

def add_comment(request, item_id):
    if request.method == "POST":
        comment = request.POST.get("comment") # get user comment
        new_comment = Comments(auction=item_id ,username=request.user.username, content=comment)
        new_comment.save()


def add_watchlist(request, id):
    item = Auction_listings.objects.get(pk=id)
    Watchlist.objects.create(user=request.user, item_id=id)
    return HttpResponseRedirect(reverse("watchlist"))


def remove_watchlist(request, id):
    item = Auction_listings.objects.get(pk=id)
    delete_item = Watchlist.objects.get(user=request.user, item=item).delete()
    return HttpResponseRedirect(reverse("watchlist"))


def view_item(request, id):
    username = request.user.username # get username
    item = Auction_listings.objects.get(pk=id)
    markdowner = markdown2.Markdown()
    description_md = markdowner.convert(item.product_description)
    
    # add bids 
    try:
        try:
            bid_value = float(Bid.objects.get(auction_name=item).bid_value).latest()
        except:
            bid_value = float(item.product_price)
    
        if request.method == "POST":
            new_bid_value = float(request.POST.get("bid"))
            if new_bid_value > bid_value:
                new_bid = Bid(auction_name=item, username=username, bid_value=new_bid_value)
                new_bid.save()
            else:
                return render(request, "auctions/error.html", {
                    "error": "your bid is lower than the current bid..."
                })

        bid = Bid.objects.get(auction_name=item)

        try:
            add_comment(request, item)
        except:
            print("no comments")
    except:
        try:
            add_comment(request, item)
        except:
            print("no comments")
        bid = ''

    try:
        watchlist = Watchlist.objects.get(user=request.user, item=item).item
    except:
        watchlist = ''

    return render(request, "auctions/item.html", {
        "auctions": item,
        "auctions_creator": str(item.username),
        "bid": bid,
        "watchlist": watchlist,
        "username": username,
        "description": description_md,
        "comments": Comments.objects.filter(auction=item)
    })


@login_required
def watchlist(request):
    items = Watchlist.objects.filter(user=request.user)
    if items:
        return render(request, "auctions/watchlist.html", {
            'products': items
        })
    else:
        return render(request, "auctions/watchlist.html", {
            'mensagem': 'Empty'
        })


def category(request):
    if request.method == "GET":
        category = request.GET.get("category")
        items = Auction_listings.objects.filter(product_category=category)
        
        return render(request, "auctions/category.html", {
            "results": items,
            "category": category
        })


def close_listing(request, page_id):
    close = Auction_listings.objects.get(pk=page_id)
    try:
        bid = Bid.objects.get(auction_name=close)
        bid_value = bid.bid_value

        if bid_value == 'None':
            return render(request, "auctions/error.html", {
                "error": "You can't close this auction without a bid"
            })

        else:
            close.is_closed = True
            close.winner = User.objects.get(username=bid.username)
            close.save()

            return render(request, "auctions/closed.html", {
                "auction": Auction_listings.objects.get(pk=page_id),
                "bid": Bid.objects.get(auction_name=close)
            })

    except Exception as e:
        if str(e) == 'Bid matching query does not exist.':
            e = "You can't close this auction without a bid."
            
        return render(request, "auctions/error.html", {
            "error": e
        })
