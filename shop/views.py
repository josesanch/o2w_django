#encoding:utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _
from sorl.thumbnail import ImageField, default
ADMIN_THUMBS_SIZE = "90x90"


class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True)
    position = models.PositiveSmallIntegerField("position")
    slug = models.CharField(max_length=255)
    image = models.ImageField(upload_to='category_imgs', blank=True)
    body = models.TextField(blank=True, verbose_name='Description')
    active = models.BooleanField()

    def __unicode__(self):
        return self.name

        
    @models.permalink
    def get_absolute_url(self):
        return ('category', [self.slug])
        
    class Meta:
        ordering = ['position']



class Product(models.Model):
    name = models.CharField(max_length=255)
    reference = models.CharField(max_length=50, blank=True, null=True)
    slug = models.SlugField(max_length=255, blank=True)
    body = models.TextField(blank=True, verbose_name='Description')
    unit_price = models.Decimal(verbose_name=_('Unit price'))
    
    active = models.BooleanField(default=True)
    offer = models.BooleanField()
    
    image = ImageField(upload_to='product_imgs', blank=True)
    position = models.PositiveSmallIntegerField("position")

    date_added = models.DateTimeField(auto_now_add=True, verbose_name=_('Date added'))
    last_modified = models.DateTimeField(auto_now=True, verbose_name=_('Last modified'))      

    category = models.ManyToManyField(Category)
    taxes = models.ManyToManyField('Taxes')
    
    
    def image_img(self):
        if self.image:
            thumb = default.backend.get_thumbnail(self.image, ADMIN_THUMBS_SIZE)
            return u'<img src="%s" />' % thumb.url
        else:
            return ''

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('product-detail', [self.tipo.slug, self.slug])

    class Meta:
        ordering = ['-id', 'name']
            
    

class Taxes(models.Model):
    name = models.CharField(max_length=255)
    value = models.FloatField()
    active = models.BooleanField(default=True)
   
        
class Order(models.Model):
    
    pass

    


class Cart(models.Model):
    pass
