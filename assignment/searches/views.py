from django.shortcuts import render
from django.views.generic import ListView
from products.models import Product
# from django.db.models import Q
# Create your views here.


class SearchProductListView(ListView):
    template_name = 'searches/view.html'

    # def get_context_data(self, *args, **kwargs):
    #     context = super(SearchProductListView, self).get_context_data(*args, **kwargs)
    #     query = self.request.GET.get('q')
    #     context['query'] = query
    #     # By this we can do more stuff like #SearchQuery.Objects.create(query=query)
    #     return context

    def get_queryset(self, *args, **kwargs):
         request = self.request
         query = request.GET.get('q', None) # request.GET is python dictionary.
         print(query)
         if query is not None:
             # lookups = Q(title__icontains=query) | Q(description__icontains=query) # Implemented this in models(#ProductModelManager(custom))
             return Product.objects.search(query) # distinct is used here to remove if we have looked up any product twice i.e one from title and one from description
         else:
             return Product.objects.none()
