# Generated by Django 4.2 on 2023-07-15 19:28

from django.db import migrations, models
import promotionApp.models


class Migration(migrations.Migration):

    dependencies = [
        ('promotionApp', '0004_alter_promotion_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotion',
            name='discount_percentage',
            field=models.IntegerField(validators=[promotionApp.models.validate_percentage]),
        ),
    ]
