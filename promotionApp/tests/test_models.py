from django.test import TestCase
from djmoney.money import Money
from django.utils import timezone
from djmoney.money import Money
from datetime import date, timedelta
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from promotionApp.models import Category, Product, Promotion

class CategoryModelTestCase(TestCase):
    def test_unique_label(self):
        category = Category.objects.create(label='Test Category')

        with self.assertRaises(Exception):
            Category.objects.create(label='Test Category')

class ProductModelTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(label="Test Category")

    def test_image_extension_validation(self):
        image = Image.new('RGB', size=(100, 100))
        temp_file = SimpleUploadedFile('test_image.bmp', image.tobytes())

        with self.assertRaises(ValidationError) as context:
            Product.objects.create(
                label="Test Product",
                image=temp_file,
                description="Test description",
                price=Money('10.0', 'EUR'),
                category=self.category
            )

        expected_error = {"image": ["Les extensions d'image autorisées sont .jpg, .jpeg, .png."]}
        self.assertEqual(context.exception.message_dict, expected_error)

    def test_image_size_validation(self):
        image = Image.new('RGB', size=(1000, 1000))
        temp_file = SimpleUploadedFile('test_image.jpg', image.tobytes())

        with self.assertRaises(ValidationError) as context:
            Product.objects.create(
                label="Test Product",
                image=temp_file,
                description="Test description",
                price=Money('10.0', 'EUR'),
                category=self.category
            )

        expected_error = {"image": ["La taille de l'image ne peut pas dépasser 2 Mo."]}
        self.assertEqual(context.exception.message_dict, expected_error)

    def test_product_creation_with_valid_values(self):
        image = Image.new('RGB', size=(500, 500))
        temp_file = SimpleUploadedFile('test_image.jpg', image.tobytes())

        product = Product.objects.create(
            label="Test Product",
            image=temp_file,
            description="Test description",
            price=Money('10.0', 'EUR'),
            category=self.category
        )

        self.assertEqual(product.label, "Test Product")
        self.assertEqual(product.price, Money('10.0', 'EUR'))
        self.assertEqual(product.category, self.category)
    
    def test_price_field(self):
        image = Image.new('RGB', size=(500, 500))
        temp_file = SimpleUploadedFile('test_image.jpg', image.tobytes())

        product = Product.objects.create(
            label="Test Product",
            image=temp_file,
            description="Test description",
            price=Money('10.0', 'EUR'),
            category=self.category
        )

        self.assertEqual(product.price, Money('10.0', 'EUR'))

        discounted_price = product.price * 0.8
        self.assertEqual(discounted_price, Money('8.0', 'EUR'))

        self.assertTrue(product.price > Money('5.0', 'EUR'))
        self.assertFalse(product.price > Money('15.0', 'EUR'))

        self.assertEqual(str(product.price), '€10.00')

    def test_required_fields(self):
        with self.assertRaises(Exception) as cm:
            Product.objects.create()

        self.assertIn('label', str(cm.exception))
        self.assertIn('description', str(cm.exception))
        self.assertIn('price', str(cm.exception))
        self.assertIn('image', str(cm.exception))
        self.assertIn('category', str(cm.exception))

class PromotionModelTestCase(TestCase):
    def setUp(self):
        self.image = Image.new('RGB', size=(500, 500))
        self.temp_file = SimpleUploadedFile('test_image.jpg', self.image.tobytes())
        self.category = Category.objects.create(label="Test Category")
        self.product = Product.objects.create(
            label="Test Product",
            image=self.temp_file,
            description="Test description",
            price=Money('10.0', 'EUR'),
            category=self.category
        )

    def test_required_fields(self):
        with self.assertRaises(Exception) as cm:
            Promotion.objects.create()

        self.assertIn('start_date', str(cm.exception))
        self.assertIn('end_date', str(cm.exception))
        self.assertIn('discount_percentage', str(cm.exception))
        self.assertIn('product', str(cm.exception))

    def test_promotion_creation_with_valid_values(self):
        start_date = date.fromisoformat("2020-01-01")
        end_date = timezone.now().date() + timedelta(days=1)

        promotion = Promotion.objects.create(
            start_date=start_date,
            end_date=end_date,
            discount_percentage=20,
            product=self.product
        )

        self.assertEqual(promotion.start_date, start_date)
        self.assertEqual(promotion.end_date, end_date)
        self.assertEqual(promotion.discount_percentage, 20)
        self.assertEqual(promotion.product, self.product)
    
    def test_discounted_price(self):
        start_date = date.fromisoformat("2020-01-01")
        end_date = timezone.now().date() + timedelta(days=1)

        promotion = Promotion.objects.create(
            start_date=start_date,
            end_date=end_date,
            discount_percentage=20,
            product=self.product
        )

        self.assertEqual(promotion.product.discounted_price, Money('8.0', 'EUR'))

    def test_delete_product(self):
        start_date = date.fromisoformat("2020-01-01")
        end_date = timezone.now().date() + timedelta(days=1)

        promotion = Promotion.objects.create(
            start_date=start_date,
            end_date=end_date,
            discount_percentage=20,
            product=self.product
        )

        self.product.delete()

        self.assertFalse(Promotion.objects.filter(pk=promotion.pk).exists())
    
    def test_delete_promotion(self):
        start_date = date.fromisoformat("2020-01-01")
        end_date = timezone.now().date() + timedelta(days=1)

        promotion = Promotion.objects.create(
            start_date=start_date,
            end_date=end_date,
            discount_percentage=20,
            product=self.product
        )

        promotion.delete()

        self.assertIsNone(promotion.product.discounted_price)