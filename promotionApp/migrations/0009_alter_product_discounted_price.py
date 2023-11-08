# Generated by Django 4.2 on 2023-07-16 18:48

from django.db import migrations
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('promotionApp', '0008_product_discounted_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='discounted_price',
            field=djmoney.models.fields.MoneyField(blank=True, decimal_places=6, default_currency='EUR', max_digits=12, null=True),
        ),
    ]
