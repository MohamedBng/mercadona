# Generated by Django 4.2 on 2023-10-13 20:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('promotionApp', '0011_alter_product_image_alter_promotion_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotion',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='promotionApp.product'),
        ),
    ]
