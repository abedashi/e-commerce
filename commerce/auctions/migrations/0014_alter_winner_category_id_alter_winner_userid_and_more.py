# Generated by Django 4.0.5 on 2022-07-23 08:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_winner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='winner',
            name='category_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.categories'),
        ),
        migrations.AlterField(
            model_name='winner',
            name='userID',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='winner',
            name='winner',
            field=models.CharField(max_length=40),
        ),
    ]
