from django.contrib import admin
from .models import User, Auction

class AuctionAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "price", "created_at", "category", "startBid", "endBid", "image")

# Register your models here.
admin.site.register(User)
admin.site.register(Auction, AuctionAdmin)