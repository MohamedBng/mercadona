# Generated by Django 4.2 on 2023-07-16 17:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('promotionApp', '0006_remove_promotion_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='promotion',
            name='product',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='promotionApp.product'),
        ),
    ]
