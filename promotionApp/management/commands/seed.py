from django.core.files import File
from django.core.management.base import BaseCommand
from promotionApp.models import Product, Category, Promotion
from djmoney.money import Money
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
import os

class Command(BaseCommand):
    help = "Seeds the database with initial data"

    def handle(self, *args, **kwargs):
        # Catégories
        categories_data = ['Aliments frais', 'Aliments emballés', 'Boissons', 'Produits de beauté et d\'hygiène', 'Nettoyage de la maison']
        for cat in categories_data:
            Category.objects.get_or_create(label=cat)

        products_data = {
            'Aliments frais': ['Poulet', 'Poisson', 'Jambon', 'Tomates', 'Laitue'],
            'Aliments emballés': ['Pâtes', 'Riz', 'Céréales', 'Conserves de thon', 'Biscuits'],
            'Boissons': ['Vin', 'Bière', 'Jus d\'orange', 'Eau', 'Limonade'],
            'Produits de beauté et d\'hygiène': ['Shampooing', 'Gel douche', 'Crème hydratante', 'Dentifrice', 'Déodorant'],
            'Nettoyage de la maison': ['Détergent', 'Nettoyant sol', 'Liquide vaisselle', 'Spray nettoyant', 'Eponge']
        }

        for cat, prods in products_data.items():
            category_instance, created = Category.objects.get_or_create(label=cat)
            for prod in prods:
                product_image_path = os.path.join(settings.BASE_DIR, 'promotionApp/static/seed_images', f"{prod}.jpg")
                if os.path.exists(product_image_path):
                    with open(product_image_path, 'rb') as image_file:
                        product_image = File(image_file)
                        product, created = Product.objects.get_or_create(
                            label=prod,
                            defaults={
                                'description': f"Description pour {prod}",
                                'price': Money(10, 'EUR'),
                                'category': category_instance,
                                'image': product_image
                            }
                        )
                else:
                    self.stdout.write(self.style.WARNING(f"L'image pour le produit {prod} n'existe pas et est ignorée."))

        self.stdout.write(self.style.SUCCESS('La base de données a été alimentée avec succès.'))
