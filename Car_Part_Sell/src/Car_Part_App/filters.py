import django_filters
from .models import Category,Car


class CategoryFilter(django_filters.FilterSet):
    class Meta:
        model = Car
        fields = ['name']
