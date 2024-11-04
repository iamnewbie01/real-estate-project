# filters.py

import django_filters
from .models import Property

class PropertyFilter(django_filters.FilterSet):
    class Meta:
        model = Property
        fields = {
            'city': ['exact'],
            'price': ['lte', 'gte'],  # Filter by price range
            'property_type': ['exact'],
            'is_rented': ['exact'],
        }
