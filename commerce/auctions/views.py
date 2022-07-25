from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from .models import User, Auction, Categories, WatchList, Bid, Comment

def index(request):
    return render(request, "auctions/index.html", {
        "Listings": Auction.objects.filter(close=False).order_by("id")[::-1],
        "Limit2": Auction.objects.filter(close=False).order_by("id")[::-1][:2],
        "CountWatchList": WatchList.objects.filter(userID=request.user.id).count()
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

@login_required(login_url='login')
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

@login_required(login_url='login')
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
                "dateerror": "date error",
                "CATEGORIES": Categories.objects.all(),
                "title": title,
                "description": description,
                "startPrice": startPrice,
                "category": category,
                "startBid": startBid,
                "endBid": endBid,
                "CountWatchList": WatchList.objects.filter(userID=request.user.id).count()
            })

        if startBid < str(datetime.now()) or endBid <= str(datetime.now()) or startBid >= endBid:
             return render(request, "auctions/createList.html", {
                "dateError": "date error",
                "CATEGORIES": Categories.objects.all(),
                "title": title,
                "description": description,
                "startPrice": startPrice,
                "category": category,
                "CountWatchList": WatchList.objects.filter(userID=request.user.id).count()
            })

        # Insert data that selected from the user to the database class Auction
        auction = Auction.objects.create(
            title=title,
            description=description,
            image=image,
            price=startPrice,
            startBid=startBid,
            endBid=endBid,
            category_id=Categories.objects.get(categories=category),
            userID=User.objects.get(id=request.user.id)
        )
        auction.save()
        messages.success(request, 'Auction added to the list Successfully.')
        return HttpResponseRedirect(reverse("createList"))

    return render(request, "auctions/createList.html", {
        "CATEGORIES": Categories.objects.all(),
        "CountWatchList": WatchList.objects.filter(userID=request.user.id).count()
    })

@login_required(login_url='login')
def categories(request):
    if request.method == "POST":
        category_id = request.POST["allCategories"]
        # Select checking
        if category_id == "Categories":
            return render(request, "auctions/categories.html", {
                "message": "SELECT CATEGORY",
                "CATEGORIES": Categories.objects.all(),
                "CountWatchList": WatchList.objects.filter(userID=request.user.id).count()
            })
        # Open category page 
        categoryone = Auction.objects.filter(category_id=Categories.objects.get(categories=category_id), close=False).order_by("id")[::-1]
        return render(request, "auctions/category.html", {
            "Categoryone": categoryone,
            "CountWatchList": WatchList.objects.filter(userID=request.user.id).count()
        })

    return render(request, "auctions/categories.html", {
        "CATEGORIES": Categories.objects.all(),
        "CountWatchList": WatchList.objects.filter(userID=request.user.id).count()
    })

@login_required(login_url='login')
def watchList(request):
    return render(request, "auctions/watchList.html", {
        "watchList": WatchList.objects.filter(userID=request.user.id).order_by("id")[::-1],
        "CountWatchList": WatchList.objects.filter(userID=request.user.id).count()
    })

@login_required(login_url='login')
def addWatchList(request, list_id):
    if request.method == "POST":
        # Preventing duplicate list in watchlist with same user
        watchList = WatchList.objects.filter(userID=request.user.id)
        if WatchList.objects.filter(auctionID=list_id, userID=request.user.id).first() in watchList:
            messages.warning(request, 'WARNING: This Auction Already in WatchList!')
            return HttpResponseRedirect(reverse("index"))

        # Create new watchlist row by inserting data same as from auction in a specific id 
        auction = Auction.objects.get(pk=list_id)
        watch = WatchList.objects.create(
            title=auction.title,
            description=auction.description,
            price=auction.price,
            image=auction.image,
            created_at=auction.created_at,
            startBid=auction.startBid,
            endBid=auction.endBid,
            category_id=Categories.objects.get(categories=auction.category_id),
            auctionID=Auction.objects.get(pk=list_id),
            userID=User.objects.get(pk=request.user.id)
        )
        watch.save()

        messages.success(request, 'Auction added to WatchList Successfully.')
        return HttpResponseRedirect(reverse("watchList"))

# Delete specific WatchList
@login_required(login_url='login')
def delete(request, list_id):
    if request.method == "POST":
        # Delete a watchlist
        if 'delete_watchList' in request.POST:
            delete = WatchList.objects.get(pk=list_id, userID=request.user.id)
            delete.delete()
            return HttpResponseRedirect(reverse("watchList"))

        # Delete closed auction from his/her owner
        elif 'delete-Winner-Auction' in request.POST:
            selectedAuction = Auction.objects.get(pk=list_id)
            selectedAuction.delete()
            return HttpResponseRedirect(reverse("winner"))

# View details of a listing
@login_required(login_url='login')
def view(request, list_id):
    return render(request, "auctions/view.html", {
        "listing": Auction.objects.get(pk=list_id),
        "countBid": Bid.objects.filter(auctionID=list_id).count(),
        "CountWatchList": WatchList.objects.filter(userID=request.user.id).count(),
        "watchList": WatchList.objects.filter(auctionID=list_id, userID=request.user.id)
    })

@login_required(login_url='login')
def bid(request, list_id):
    if request.method == "POST":
        bid = float(request.POST["bid"])

        if not bid:
            return render(request, "auctions/view.html")

        # Check price for biding
        updateBidAuction = Auction.objects.get(pk=list_id)
        updateBidWatchList = WatchList.objects.filter(auctionID=Auction.objects.get(pk=list_id))
        if bid <= updateBidAuction.price:
            messages.warning(request, 'WARNING: Bid Must be greater than old price')
            return HttpResponseRedirect(reverse("view", args=(list_id,)))

        # Iterate through updateBidWatchlist to update all the watchlist price that are biding
        for row in updateBidWatchList:
            if bid <= row.price:
                messages.warning(request, 'WARNING: Bid Must be greater than old price')
                return HttpResponseRedirect(reverse("viewWatchList"))
            row.price = bid
            row.save()

        # update auction price
        updateBidAuction.price = bid
        updateBidAuction.save()

        # Create new row in Bid model
        newPrice = Bid.objects.create(
            price=bid,
            userID=User.objects.get(pk=request.user.id),
            auctionID=Auction.objects.get(pk=list_id)
        )
        newPrice.save()
        return HttpResponseRedirect(reverse("view", args=(list_id,)))

@login_required(login_url='login')
def comment(request, list_id):
    if request.method == "POST":

        # Attempt to sign user in
        comment = request.POST["comment"]
        if not comment:
            messages.warning(request, 'Place a Comment.')
            return HttpResponseRedirect(reverse("index"))
        
        # Insert comment fields
        commentRow = Comment.objects.create(
            comment=comment,
            auctionID=Auction.objects.get(pk=list_id),
            userID=User.objects.get(pk=request.user.id)
        )
        commentRow.save()
        
    return render(request, "auctions/comment.html", {
        "listing": Auction.objects.get(pk=list_id),
        "comments": Comment.objects.filter(auctionID=list_id).order_by("id")[::-1],
        "CountWatchList": WatchList.objects.filter(userID=request.user.id).count()
    })

@login_required(login_url='login')
def myAuctions(request):
    return render(request, "auctions/myAuctions.html", {
        "myAuctions": Auction.objects.filter(userID=request.user.id, close=False),
        "CountWatchList": WatchList.objects.filter(userID=request.user.id).count()
    })

@login_required(login_url='login')
def closeAuction(request, list_id):
    # checking if this auction have been bidded from any user
    myAuctionSelected = Auction.objects.get(pk=list_id)
    bids = Bid.objects.all()
    if not Bid.objects.filter(auctionID=list_id, price=myAuctionSelected.price).first() in bids:
        myAuctionSelected.close = True
        myAuctionSelected.save()

        messages.warning(request, 'No One Wins This Auction')
        return HttpResponseRedirect(reverse("myAuctions"))

    # Auction update close to True and update winner 
    usernameOfHighestBid = Bid.objects.get(auctionID=list_id, price=myAuctionSelected.price)
    myAuctionSelected.close = True
    myAuctionSelected.winner = User.objects.get(pk=usernameOfHighestBid.userID.id)
    myAuctionSelected.save()

    # announcement to check the winner
    messages.warning(request, 'Check Who is the Winner')
    return HttpResponseRedirect(reverse("myAuctions"))
    
@login_required(login_url='login')
def winner(request):
    return render(request, "auctions/winner.html", {
        "winner": Auction.objects.filter(close=True).order_by("id")[::-1],
        "CountWatchList": WatchList.objects.filter(userID=request.user.id).count()
    })
