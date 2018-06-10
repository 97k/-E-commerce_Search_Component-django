from django.shortcuts import render
from django.views.generic import ListView
from products.models import Product
from django.db.models import Avg, Max, Min

# Create your views here.

_query = ''
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
         _query = query
         print('_query is set to ', _query)
         print(query)
         if query is not None:
             # lookups = Q(title__icontains=query) | Q(description__icontains=query) # Implemented this in models(#ProductModelManager(custom))
             return Product.objects.search(query) # distinct is used here to remove if we have looked up any product twice i.e one from title and one from description
         else:
             return Product.objects.none()

    # class priceFilter(low_price=0, high_price=0):
    #
    #     if low_price<high_price:
    #         lp = Q(price__lte=high_price)
    #         hp = Q(price__gte=low_price)
    #         return Product.objects.search(_query).filter(lp & hp)


class PriceFilter(ListView):
    template_name = 'searches/view.html'

    def get_queryset(self, *args, **kwargs):
        request = self.request
        # lp = request.GET.get('low-price', None) # request.GET is python dictionary.
        # hp = request.GET.get('high-price', None)
        # print('low_price: ', lp, 'high_price', hp)
        # if lp<hp:
        #     low_price = Q(price__lte=high_price)
        #     high_price = Q(price__gte=low_price)
        #     print('this is what we found', low_price, high_price)
        #     return Product.objects.search(_query).filter(lp & hp)
        # else:
        #     return Product.objects.none()

        if 'low_price' in request.GET:
            filter_price1 = request.GET.get('low_price')
            filter_price2 = request.GET.get('high_price')
            if filter_price1 =='':
                filter_price1=0
            if filter_price2=='':
                filter_price2=Product.objects.search(_query).aggregate(Max('price'))
                filter_price2 = filter_price2.get('price__max')
            my_products=Product.objects.search(_query).filter_price(low_price=filter_price1, high_price=filter_price2)
            print('My products after applying filter are', my_products)
            return my_products
