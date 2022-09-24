import django_filters
from .models import *
from django_filters import CharFilter
from django import forms

BIRTH_YEAR_CHOICES = ['1980', '1981', '1982']
FAVORITE_COLORS_CHOICES = [
    ('blue', 'Blue'),
    ('green', 'Green'),
    ('black', 'Black'),
]

class JobPostFilter(django_filters.FilterSet):
    job_title = CharFilter(field_name='job_title', lookup_expr='icontains', widget=forms.TextInput(attrs={"class":"form-control", 'placeholder': 'Job Title..'}))
    city = CharFilter(field_name='city', lookup_expr='icontains', widget=forms.TextInput(attrs={"class":"form-control", 'placeholder': 'City..'}))
    tag = CharFilter(field_name='tag', lookup_expr='icontains', widget=forms.TextInput(attrs={"class":"form-control", 'placeholder': 'Tag..'}))
    class Meta:
        model = JobPost
        fields = ['job_title', 'city']
