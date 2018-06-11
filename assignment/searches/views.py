from django.shortcuts import render
from django.views.generic import ListView
from products.models import Product, Category
from tags.models import Tag
from django.db.models import Avg, Max, Min, Q

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
        _query = request.GET.get('prev')
        print('changed to ', _query)
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
            low_price = request.GET.get('low_price')
            max_price = request.GET.get('high_price')

            if low_price =='':
                low_price=0
            if max_price=='':
                # max_price = Tag.objects.get(Q(title__icontains=_query)).products.aggregate(Max('price'))
                if len(_query.split())>1:
                    q = _query.split()
                    print(q)

                    for value in q:
                        print(value)
                        print('looking in ', _query)
                        max_price = Category.objects.filter(Q(title__icontains=_query)|Q(description__icontains=_query))
                        max_price = max_price.first()
                        print(max_price)
                        max_price = max_price.products.aggregate(Max('price'))
                        print(max_price)


                        if max_price is not None:
                            print('filter price 2 is found and is ', max_price)
                            return

                else:
                    print('looking in ', _query)
                    max_price = Category.objects.filter(Q(title__icontains=_query)|Q(description__icontains=_query))
                    max_price = max_price.first()
                    print(max_price)
                    max_price = max_price.products.aggregate(Max('price'))
                    print(max_price)
                    #
                    # if  len(max_price) != 1:
                    #     max_price=Product.objects.search(_query).aggregate(Max('price'))

                    max_price = max_price.get('price__max')
                    print(max_price)

            my_products=Product.objects.search(_query).filter_price(low_price=low_price, high_price=max_price)
            print('My products after applying filter are', my_products)
            return my_products
