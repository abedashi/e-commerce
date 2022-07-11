from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Auction(models.Model):
    title = models.CharField(max_length=40)
    description = models.CharField(max_length=1000)
    category = models.CharField(max_length=40)
    created_at = models.DateTimeField(default=timezone.now)
    image = models.URLField(max_length=200)
    price = models.FloatField()
    startBid = models.DateTimeField(auto_now=False, auto_now_add=False)
    endBid = models.DateTimeField(auto_now=False, auto_now_add=False)
    # user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="buyer")

    def __str__(self):
        return f"{self.title}, {self.description}, {self.category}, {self.created_at}, {self.image}, ${self.price}, {self.startBid}, {self.endBid}"