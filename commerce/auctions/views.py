from datetime import datetime, timezone
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from .models import User, Auction, Categories

# @login_required
def index(request):
    return render(request, "auctions/index.html", {
        "Listings": Auction.objects.all()
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

# Categories List Fields
# CATEGORIES = [
#             "Jewelry & Watches", "Furniture, Appliances & Equipment", "Video Games, Consoles & Accessories",
#             "Flowers, Greetings & Misc Gifts", "Event Tickets", "Computer Software", "Home & Garden",
#             "Music, Movies & videos", "Apparel & Accessories", "Total Digital Commerce", "Office Supplies",
#             "Consumer Packaged Goods", "Sport & Fitness", "Toys & Hobbies", "Consumer Electronics",
#             "Digital Content & Subscriptions", "Computers / Peripherals / PDAs", "Books & Magazines", "Others"
#         ]

@login_required(redirect_field_name='index')
def createList(request):
    if request.method == "POST":

        # Attempt Creating Auction
        title = request.POST["title"]
        description = request.POST["description"]
        image = request.POST["url"]
        startPrice = request.POST["price"]
        category = request.POST["categories"]
        startBid = request.POST["startBid"]
        endBid = request.POST["endBid"]

        # Check for category if selected or gives a message and more security
        if not title or not description or not image or not startPrice or category == "Categories" or not startBid or not endBid:
            return render(request, "auctions/createList.html", {
                "message": "Select a Category",
                "CATEGORIES": Categories.objects.all(),
                "title": title,
                "description": description,
                "image": image,
                "startPrice": startPrice,
                "category": category,
                "startBid": startBid,
                "endBid": endBid
            })
        
        # Insert data that selected from the user to the database class Auction
        try:
            auction = Auction.objects.create(
                title=title,
                description=description,
                image=image,
                price=startPrice,
                startBid=startBid,
                endBid=endBid,
                category_id=Categories.objects.get(categories=category)
            )
            auction.save()
            messages.success(request, 'Auction added to the list Successfully.')
            return HttpResponseRedirect(reverse("createList"))
        except Exception as e:
            messages.warning(request, 'Auction Failed to the list Successfully.')

    return render(request, "auctions/createList.html", {
        "CATEGORIES": Categories.objects.all()
    })

def categories(request):
    if request.method == "POST":
        category_id = int(request.POST["allCategories"])
        if not category_id:
            return render(request, "auctions/categories.html", {
                "message": "SELECT CATEGORY",
                "CATEGORIES": Categories.objects.all()
            })
        categoryone = Auction.objects.filter(category_id=category_id)
        return render(request, "auctions/category.html", {
            "Categoryone": categoryone
        })

    return render(request, "auctions/categories.html", {
        "CATEGORIES": Categories.objects.all()
    })

def watchList(request):
    return render(request, "auctions/watchList.html")

def addWatchList(request, list_id):
    return render(request, "auctions/.html")

def view(request, list_id):
    return render(request, "auctions/view.html", {
        "listing": Auction.objects.get(pk=list_id)
    })
