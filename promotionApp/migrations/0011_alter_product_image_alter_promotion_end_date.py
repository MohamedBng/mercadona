# Generated by Django 4.2 on 2023-08-13 02:10

from django.db import migrations, models
import promotionApp.models


class Migration(migrations.Migration):

    dependencies = [
        ('promotionApp', '0010_alter_product_discounted_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(upload_to='', validators=[promotionApp.models._validate_image_size, promotionApp.models._validate_image_extension]),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='end_date',
            field=models.DateField(validators=[promotionApp.models.validate_future_date]),
        ),
    ]
