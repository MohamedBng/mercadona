import os
import django
from promotionApp.models import Product, Category, Promotion
from djmoney.money import Money
from django.utils import timezone
from datetime import timedelta
from django.db import transaction

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mercadona.settings")
django.setup()

@transaction.atomic
def run():
    categories_data = ['Aliments frais', 'Aliments emballés', 'Boissons', 'Produits de beauté et d\'hygiène', 'Nettoyage de la maison']
    categories = [Category(label=cat) for cat in categories_data]
    Category.objects.bulk_create(categories)

    products_data = {
        'Aliments frais': ['Poulet', 'Poisson', 'Jambon', 'Tomates', 'Laitue'],
        'Aliments emballés': ['Pâtes', 'Riz', 'Céréales', 'Conserves de thon', 'Biscuits'],
        'Boissons': ['Vin', 'Bière', 'Jus d\'orange', 'Eau', 'Limonade'],
        'Produits de beauté et d\'hygiène': ['Shampooing', 'Gel douche', 'Crème hydratante', 'Dentifrice', 'Déodorant'],
        'Nettoyage de la maison': ['Détergent', 'Nettoyant sol', 'Liquide vaisselle', 'Spray nettoyant', 'Eponge']
    }

    for cat, prods in products_data.items():
        category_instance = Category.objects.get(label=cat)
        for prod in prods:
            Product.objects.create(label=prod, description=f"Description pour {prod}", price=Money(10, 'EUR'), category=category_instance)

    for cat in categories_data:
        category_instance = Category.objects.get(label=cat)
        products_in_category = Product.objects.filter(category=category_instance)[:2]
        for prod in products_in_category:
            Promotion.objects.create(start_date=timezone.now().date(), end_date=timezone.now().date() + timedelta(days=10), discount_percentage=10, product=prod)

if __name__ == '__main__':
    run()