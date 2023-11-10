import os
import django
from django.core.files import File

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mercadona.settings")
django.setup()

from promotionApp.models import Product, Category, Promotion
from djmoney.money import Money
from django.utils import timezone
from datetime import timedelta
from django.db import transaction

@transaction.atomic
def run():
    print("Début du script de seeding...")

    categories_data = ['Aliments frais', 'Aliments emballés', 'Boissons', 'Produits de beauté et d\'hygiène', 'Nettoyage de la maison']
    Category.objects.bulk_create([Category(label=cat) for cat in categories_data if not Category.objects.filter(label=cat).exists()])
    print(f"Catégories créées : {categories_data}")

    products_data = {
        'Aliments frais': ['Poulet', 'Poisson', 'Jambon', 'Tomates', 'Laitue'],
        'Aliments emballés': ['Pâtes', 'Riz', 'Céréales', 'Conserves de thon', 'Biscuits'],
        'Boissons': ['Vin', 'Bière', 'Jus d\'orange', 'Eau', 'Limonade'],
        'Produits de beauté et d\'hygiène': ['Shampooing', 'Gel douche', 'Crème hydratante', 'Dentifrice', 'Déodorant'],
        'Nettoyage de la maison': ['Détergent', 'Nettoyant sol', 'Liquide vaisselle', 'Spray nettoyant', 'Eponge']
    }

    for cat, prods in products_data.items():
        category_instance = Category.objects.get(label=cat)
        print(f"Traitement de la catégorie : {cat}")
        for prod in prods:

            image_path = os.path.join('promotionApp/_static/seed_images', f"{prod}.jpg") 
            if os.path.exists(image_path): # vérifiez l'existence de l'image
                with open(image_path, 'rb') as img_file:
                    product_image = File(img_file)
                    product, created = Product.objects.get_or_create(
                        label=prod,
                        defaults={
                            'description': f"Description pour {prod}",
                            'price': Money(10, 'EUR'),
                            'category': category_instance,
                            'image': product_image
                        }
                    )
                    if created:
                        print(f"Produit créé : {prod} avec l'image {product_image.name} dans la catégorie {cat}")
            else:
                print(f"L'image pour {prod} n'existe pas à l'emplacement {image_path}. Utilisation d'une image par défaut ou saut de l'image.")

    for cat in categories_data:
        category_instance = Category.objects.get(label=cat)
        products_in_category = Product.objects.filter(category=category_instance)[:2]
        print(f"Produits trouvés pour la promotion dans la catégorie {cat}: {[p.label for p in products_in_category]}")
        for prod in products_in_category:
            promotion, created = Promotion.objects.get_or_create(
                product=prod,
                defaults={
                    'start_date': timezone.now().date(),
                    'end_date': timezone.now().date() + timedelta(days=10),
                    'discount_percentage': 10
                }
            )
            if created:
                print(f"Promotion créée pour : {promotion.product.label} avec une réduction de {promotion.discount_percentage}%")

    print("Script de seeding terminé.")

if __name__ == "__main__":
    run()
