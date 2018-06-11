from django.shortcuts import render
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView


from .models import Product
import random

# Create your views here.


class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    # queryset = Product.objects.all()

    def get_queryset(self, *args, **kwargs):
        request = self.request
        items = sorted(Product.objects.all(), key=lambda x: random.random())
        return  items #Then we can get rid of the queryset call at the beginning of this class which is now commented.
