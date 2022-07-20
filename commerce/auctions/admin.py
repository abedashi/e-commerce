from django.contrib import admin
from .models import User, Auction, Categories, WatchList

class AuctionAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "userID", "category_id")

class CategoriesAdmin(admin.ModelAdmin):
    list_display = ("id", "categories")

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "password", "is_superuser")

class WatchListAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "auctionID", "category_id", "userID")

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Auction, AuctionAdmin)
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(WatchList, WatchListAdmin)