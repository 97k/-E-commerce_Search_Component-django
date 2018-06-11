from django.shortcuts import render
from django.views.generic import ListView
from products.models import Product, Category
from tags.models import Tag
from django.shortcuts import Http404
from django.db.models import Avg, Max, Min, Q

# Create your views here.

_query = ''
class SearchProductListView(ListView):
    template_name = 'searches/view.html'

    def get_context_data(self, *args, **kwargs):
        context = super(SearchProductListView, self).get_context_data(*args, **kwargs)
        request = self.request
        content = request.GET.get('q')
        try:
            if len(content.split())>1:
                content = content.split()
                for value in content:
                    obj = Category.objects.filter(Q(title__icontains=value)|Q(description__icontains=value))
                    if obj.first().title=='Mobile':
                        context['content']='mobile'
                        context['android']='Android'
                        context['iOS'] = 'iOS'
                        break
            else:

                    obj = Category.objects.filter(Q(title__icontains=content)|Q(description__icontains=content))
                    if obj.first().title=='Mobile':
                        context['content'] = 'mobile'
                        context['android']='Android'
                        context['iOS'] = 'iOS'
        except:
            raise Http404('Sorry! We do not have this product!')
        return context


    def get_queryset(self, *args, **kwargs):
         request = self.request
         query = request.GET.get('q', None) # request.GET is python dictionary.
         if query is not None:
            #Implemented this in models ProductModelManager(custom))
             return Product.objects.search(query)
         else:
             return Product.objects.none()


class Filter(ListView):
    template_name = 'searches/view.html'

    def get_queryset(self, *args, **kwargs):
        request = self.request
        _query = request.GET.get('prev')

        if 'low_price' in request.GET:
            low_price = request.GET.get('low_price')
            max_price = request.GET.get('high_price')

            if 'Android' in request.GET:
                _query = 'android'
            if 'iOS' in request.GET:
                _query = 'iOS'

            if low_price =='':
                low_price=0
            if max_price=='':
                if len(_query.split())>1:
                    q = _query.split()

                    for value in q:
                        print(value)
                        print('looking in ', _query)
                        obj = Category.objects.filter(Q(title__icontains=_query)|Q(description__icontains=_query))
                        max_price = obj.first()
                        print(max_price)
                        max_price = max_price.products.aggregate(Max('price'))
                        print(max_price)


                        if max_price is not None:
                            print('filter price 2 is found and is ', max_price)
                            break

                else:
                    print('looking in ', _query)
                    obj = Category.objects.filter(Q(title__icontains=_query)|Q(description__icontains=_query))
                    max_price = obj.first()
                    print(max_price)
                    max_price = max_price.products.aggregate(Max('price'))
                    print(max_price)
                    #
                    if  len(max_price) != 1:
                        max_price=Product.objects.search(_query).aggregate(Max('price'))

                    max_price = max_price.get('price__max')
                    print(max_price)

            my_products=Product.objects.search(_query).filter_price(low_price=low_price, high_price=max_price)
            print('My products after applying filter are', my_products)
            return my_products

        if 'Android' in request.GET:
            return Product.objects.search('android')
        elif 'iOS' in request.GET:
            return Product.objects.search('iOS')
