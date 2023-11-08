import os
import django
from django.core.management import call_command
from promotionApp.models import Product, Category, Promotion
from djmoney.money import Money
from django.utils import timezone
from datetime import timedelta

# Initialisez Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mercadona.settings")
django.setup()

class Command(BaseCommand):
    help = 'Seeds the database with initial data'

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

        default_image_path = 'muffin-g989da0f83_640_v9CY5WK.jpg'

        for cat, prods in products_data.items():
            category_instance = Category.objects.get(label=cat)
            for prod in prods:
                Product.objects.get_or_create(
                    label=prod,
                    defaults={
                        'description': f"Description pour {prod}",
                        'price': Money(10, 'EUR'),
                        'category': category_instance,
                        'image': f"{prod}.jpg"
                    }
                )

        for cat in categories_data:
            category_instance = Category.objects.get(label=cat)
            products_in_category = Product.objects.filter(category=category_instance)[:2]
            for prod in products_in_category:
                Promotion.objects.get_or_create(
                    product=prod,
                    defaults={
                        'start_date': timezone.now().date(),
                        'end_date': timezone.now().date() + timedelta(days=10),
                        'discount_percentage': 10
                    }
                )
