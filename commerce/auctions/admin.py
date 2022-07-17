from django.contrib import admin
from .models import User, Auction, Categories

class AuctionAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "category_id", "price", "created_at", "startBid", "endBid", "image")

class CategoriesAdmin(admin.ModelAdmin):
    list_display = ("id", "categories")

# Register your models here.
admin.site.register(User)
admin.site.register(Auction, AuctionAdmin)
admin.site.register(Categories, CategoriesAdmin)