from django.contrib import admin
from .models import User, Auction, Categories, WatchList, Bid, Comment

class AuctionAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "close", "winner", "userID", "category_id", "price", "startBid", "endBid", "image")

class CategoriesAdmin(admin.ModelAdmin):
    list_display = ("id", "categories")

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "password", "is_superuser")

class WatchListAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "auctionID", "category_id", "userID", "price")

class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "price", "auctionID", "userID")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "comment", "userID", "auctionID", "time")

class WinnerAdmin(admin.ModelAdmin):
    list_display = ("id", "winner", "userID", "title", "price")

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Auction, AuctionAdmin)
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(WatchList, WatchListAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)