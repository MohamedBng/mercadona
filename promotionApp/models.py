import os
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from decimal import Decimal
from django.utils import timezone
from djmoney.money import Money
from djmoney.models.fields import MoneyField
from django.db import models
from django.core.exceptions import ValidationError

# Fonction de validation de la taille de l'image
def _validate_image_size(value):
    if value.size > 2097152:  # 2 Mo en octets
        raise ValidationError("La taille de l'image ne peut pas dépasser 2 Mo.")

# Fonction de validation de l'extension de l'image
def _validate_image_extension(value):
    valid_extensions = ['.jpg', '.jpeg', '.png']
    ext = os.path.splitext(value.name)[1].lower()
    if ext not in valid_extensions:
        raise ValidationError("Les extensions d'image autorisées sont .jpg, .jpeg, .png.")

# Fonction de validation du pourcentage
def validate_percentage(value):
    if value < 0 or value > 100:
        raise ValidationError('Le pourcentage doit être compris entre 0 et 100.')

# Fonction de validation de la date future
def validate_future_date(value):
    if value < timezone.now().date():
        raise ValidationError("La date ne peut pas être dans le passé.")

# Modèle Category
class Category(models.Model):
    label = models.CharField(max_length=255, unique=True)

    def clean(self):
        if not self.label:
            raise ValidationError("Le champ label est obligatoire.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.label

# Modèle Product
class Product(models.Model):
    label = models.CharField(max_length=255)
    description = models.TextField()
    price = MoneyField(max_digits=4, decimal_places=2, default_currency='EUR')
    image = models.ImageField(validators=[_validate_image_size, _validate_image_extension])
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    # Propriété calculée pour obtenir l'URL de l'image
    @property
    def image_url(self):
        if self.image:
            url = f"http://localhost:3000/images/{os.path.basename(self.image.name)}"
            print(f"Image URL: {url}")  # Ajoutez cette ligne pour le débogage
            return url
        return ''

    def clean(self):
        required_fields = {
            'label': 'Le champ {} est obligatoire.',
            'description': 'Le champ {} est obligatoire.',
            'price': 'Le champ {} est obligatoire.',
            'image': 'Le champ {} est obligatoire.',
            'category_id': 'Le champ {} est obligatoire.',
        }

        missing_fields = []
        for field, error_message in required_fields.items():
            if not getattr(self, field):
                missing_fields.append(error_message.format(field))

        if missing_fields:
            raise ValidationError(missing_fields)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.label

    def get_active_promotion(self):
        current_date = timezone.now().date()
        promotions = self.promotion_set.filter(start_date__lte=current_date, end_date__gte=current_date)
        return promotions.first() if promotions.exists() else None

# Modèle Promotion
class Promotion(models.Model):
    start_date = models.DateField()
    end_date = models.DateField(validators=[validate_future_date])
    discount_percentage = models.IntegerField(validators=[validate_percentage])
    discounted_price = MoneyField(max_digits=4, decimal_places=2, default_currency='EUR', blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def clean(self):
        required_fields = {
            'start_date': 'Le champ {} est obligatoire.',
            'end_date': 'Le champ {} est obligatoire.',
            'discount_percentage': 'Le champ {} est obligatoire.',
            'product_id': 'Le champ {} est obligatoire.',
        }

        missing_fields = []
        for field, error_message in required_fields.items():
            if not getattr(self, field):
                missing_fields.append(error_message.format(field))

        if missing_fields:
            raise ValidationError(missing_fields)

        overlapping_promotions = Promotion.objects.filter(
            product=self.product,
            start_date__lte=self.end_date,
            end_date__gte=self.start_date
        )

        if self.pk:
            overlapping_promotions = overlapping_promotions.exclude(pk=self.pk)

        if overlapping_promotions.exists():
            raise ValidationError("Il y a déjà une promotion pour ce produit pendant la période spécifiée.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    # Méthode pour changer le prix du produit en fonction de la promotion
    def change_price(self):
        self.discounted_price *= (1 - self.discount_percentage / 100)
        self.save()

    def __str__(self):
        return self.discount_percentage.__str__() + "%"

# Signal pour mettre à jour le prix remisé du produit après avoir enregistré une promotion
@receiver(post_save, sender=Promotion)
def update_discounted_price(sender, instance, created, **kwargs):
    if instance.product:
        discount_percentage = Decimal(instance.discount_percentage) / 100
        price_amount = Decimal(str(instance.product.price.amount))
        discounted_amount = price_amount * (1 - discount_percentage)
        instance.product.discounted_price = Money(amount=discounted_amount.quantize(Decimal('.01')), currency=instance.product.price_currency)
        instance.product.save()

# Signal pour réinitialiser le prix remisé du produit avant de supprimer une promotion
@receiver(pre_delete, sender=Promotion)
def reset_discounted_price(sender, instance, **kwargs):
    if instance.product:
        instance.product.discounted_price = None
        instance.product.save()
