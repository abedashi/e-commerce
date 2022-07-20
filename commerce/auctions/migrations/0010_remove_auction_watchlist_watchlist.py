# Generated by Django 4.0.5 on 2022-07-20 04:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_auction_watchlist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auction',
            name='watchList',
        ),
        migrations.CreateModel(
            name='WatchList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40)),
                ('description', models.CharField(max_length=1000)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('image', models.URLField(max_length=400)),
                ('price', models.FloatField()),
                ('startBid', models.DateTimeField()),
                ('endBid', models.DateTimeField()),
                ('auctionID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auctions.auction')),
                ('category_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auctions.categories')),
                ('userID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
