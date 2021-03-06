from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Categories(models.Model):
    categories = models.CharField(max_length=70)

    def __str__(self):
        return f"{self.categories}"

class Auction(models.Model):
    title = models.CharField(max_length=40)
    description = models.CharField(max_length=1000)
    created_at = models.DateTimeField(default=timezone.now)
    image = models.ImageField(null=True, blank=True)
    price = models.FloatField()
    startBid = models.DateTimeField(auto_now=False, auto_now_add=False)
    endBid = models.DateTimeField(auto_now=False, auto_now_add=False)
    userID = models.ForeignKey(User, on_delete=models.CASCADE, related_name="buyer", null=True)
    category_id = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="categoryId", null=True)
    close = models.BooleanField(default=False)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"({self.title}, {self.description}, {self.category_id})"

class WatchList(models.Model):
    title = models.CharField(max_length=40)
    description = models.CharField(max_length=1000)
    created_at = models.DateTimeField(default=timezone.now)
    image = models.ImageField(null=True, blank=True)
    price = models.FloatField()
    startBid = models.DateTimeField(auto_now=False, auto_now_add=False)
    endBid = models.DateTimeField(auto_now=False, auto_now_add=False)
    userID = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    category_id = models.ForeignKey(Categories, on_delete=models.CASCADE, null=True)
    auctionID = models.ForeignKey(Auction, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.id}, {self.auctionID}, {self.userID}"

class Bid(models.Model):
    price = models.FloatField()
    userID = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    auctionID = models.ForeignKey(Auction, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.id}, {self.userID}, {self.auctionID}"

class Comment(models.Model):
    comment = models.CharField(max_length=1000)
    time = models.DateTimeField(default=timezone.now)
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    auctionID = models.ForeignKey(Auction, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id}, {self.comment}, {self.time}, {self.userID}, {self.auctionID}"