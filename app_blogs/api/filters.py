from django_filters.rest_framework import FilterSet
from django_filters.filters import CharFilter, DateTimeFilter, NumberFilter, BaseInFilter

from app_blogs.models import Post

class NumberInFilter(BaseInFilter, NumberFilter):
    pass

class PostFilter(FilterSet):
    categories = NumberInFilter(field_name='category', lookup_expr='in')
    tags = NumberInFilter(field_name="tags", lookup_expr='in')
    start_date = DateTimeFilter(field_name='created_at', lookup_expr='gte') 
    end_date = DateTimeFilter(field_name='created_at', lookup_expr='lte') 

    class Meta:
        model = Post
        fields = {
            'category': ['exact'],
            'tags': ['exact', 'contains'],
            'status': ['exact'],
            'created_at': ['gt', 'lt']
        }
