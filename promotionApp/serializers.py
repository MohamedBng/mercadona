from rest_framework import serializers
from .models import Product
from .models import Category
from .models import Promotion

class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = ['id', 'start_date', 'end_date', 'discount_percentage', 'product']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    active_promotion = PromotionSerializer(source='get_active_promotion', read_only=True)
    
    class Meta:
        model = Product
        fields = ('id', 'label', 'description', 'price_currency', 'price', 'image_url', 'category', 'active_promotion')

    def get_image_url(self, obj):
    if obj.image:
        return obj.image.url
    return None