from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
import random
import os

# Unique slug unique_slug_generator
from .utils import unique_slug_generator
# Create your models here.

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    # print(instance)
    # print(filename)
    new_filename = random.randint(1, 8378437483)
    name, ext = get_filename_ext(filename)
    # final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    # for python 3.6 we can do something like this.
    final_filename = f'{new_filename}{ext}'
    return f'products/{new_filename}/{final_filename}'





class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(feature=True, active=True)

    def search(self, query):
        lookups = (Q(title__icontains=query)|
                    Q(description__icontains=query)|
                    Q(tag__title__icontains=query)|
                    Q(tag__slug__icontains=query)
                    )
        return self.filter(lookups).distinct()

    def filter_price(self, low_price, high_price):
        return self.filter(price__range=(low_price, high_price))

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

# by this we can do like this Products.objects.featured
# and with custom query set we can have something just like this -> Prodcut.objects.filter(title__icontains='supercomputer').featured()
    def featured(self):
        return self.get_queryset().featured()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id) # This takes portion of products.objects self.get_queryset( )
        if qs.count()==1:
            return qs.first() # This is the individual instance of the object
        return None

    def search(self, query):
        return self.get_queryset().active().search(query)



class Product(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, unique=True)
    description = models.TextField()
    # I've added a default value as per the suggestions given by django.(39.99)
    price = models.DecimalField(decimal_places=2, max_digits=20, default=39.99)
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    feature = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)


    # def get_absolute_url(self):
    #     # return '/products/{slug}'.format(slug=self.slug) The best way is to use reverseself.
    #     return reverse('products:detail', kwargs={'slug': self.slug, })

    objects = ProductManager() # This objects field comes from the context or to be more precise from default  model manager. It is an attribute form the get_context_data
    def __str__(self):
        return self.title


def product_pre_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save, sender=Product)
