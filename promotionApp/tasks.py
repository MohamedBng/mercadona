from datetime import date
from django.utils import timezone
from .models import Promotion
from celery import shared_task

@shared_task()
def delete_expired_promotions():
    expired_promotions = Promotion.objects.filter(end_date__lt=date.today())
    for promotion in expired_promotions:
        if promotion.end_date < date.today():
            promotion.delete()
