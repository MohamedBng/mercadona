from django.shortcuts import redirect
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from .models import Product
from .models import Category
from .models import Promotion
from .serializers import CategorySerializer
from .serializers import ProductSerializer
from .serializers import PromotionSerializer
from django_filters.rest_framework import DjangoFilterBackend

def redirect_to_admin(request):
    return redirect('/admin/')

class PromotionList(generics.ListCreateAPIView):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer

class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductList(generics.ListAPIView):
    queryset = Product.objects.order_by('id')  # Tri par ID (choisissez le champ approprié)
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        promotion = self.request.query_params.get('promotion', None)
        if promotion == 'true':
            queryset = queryset.filter(discounted_price__isnull=False)
        elif promotion == 'false':
            queryset = queryset.filter(discounted_price__isnull=True)
        
        return queryset

