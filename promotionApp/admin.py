from django import forms
from django.contrib import admin
from .models import Category, Product, Promotion

class PromotionInlineForm(forms.ModelForm):
    class Meta:
        model = Promotion
        fields = ['start_date', 'end_date', 'discount_percentage']


class PromotionInline(admin.StackedInline):
    model = Promotion
    form = PromotionInlineForm
    can_delete = True
    verbose_name_plural = 'Promotion'
    fieldsets = [
        ('Promotion Information', {'fields': ['start_date', 'end_date', 'discount_percentage']}),
    ]


class ProductAdmin(admin.ModelAdmin):
    inlines = [PromotionInline]

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
