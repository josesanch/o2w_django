#encoding:utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from filer.fields.image import FilerImageField, FilerFileField
from fields import CurrencyField
from o2w.comments.models import CommentWithRatings
import datetime
from django.db.models import Avg
from django.contrib.contenttypes.models import ContentType
from managers import OrderManager
from django.db.models import Q


ADMIN_THUMBS_SIZE = "90x90"


class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True)

    slug = models.CharField(max_length=255)
    image = models.ImageField(upload_to='category_imgs', blank=True)
    body = models.TextField(blank=True, verbose_name='Description')
    active = models.BooleanField(default=True)
    position = models.PositiveSmallIntegerField("position", blank=True, null=True)

    def __unicode__(self):
        return self.name


    @models.permalink
    def get_absolute_url(self):
        return ('category', [self.slug])

    class Meta:
        ordering = ['position']
        verbose_name_plural = 'Categories'

class ActiveProduct(models.Manager):
    def get_query_set(self):
        return super(ActiveProduct, self)\
            .get_query_set()\
            .filter(active=True)


class Product(models.Model):
    name = models.CharField(max_length=255)
    reference = models.CharField(max_length=50, blank=True, null=True)
    slug = models.SlugField(max_length=255, blank=True)
    body = models.TextField(blank=True, verbose_name='Description')
    unit_price = CurrencyField(verbose_name=_('Unit price'))

    active = models.BooleanField(default=True)
    offer = models.BooleanField()

    # Dimensions
    height = models.FloatField(null=True, blank=True)
    length = models.FloatField(null=True, blank=True)
    width = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    capacity = models.FloatField(null=True, blank=True)
    diameter = models.FloatField(null=True, blank=True)

    image = FilerImageField(null=True, blank=True, related_name='images')

    position = models.PositiveSmallIntegerField("position", blank=True, null=True)

    date_added = models.DateTimeField(auto_now_add=True, verbose_name=_('Date added'))
    last_modified = models.DateTimeField(auto_now=True, verbose_name=_('Last modified'))

    category = models.ManyToManyField(Category)
    taxes = models.ManyToManyField('Tax', null=True, blank=True)
    absolute_url = models.CharField(max_length=255, blank=True, null=True)

    objects = ActiveProduct()
    includeinactive = models.Manager()


    def __unicode__(self):
        return self.name

    def get_absolute_slug(self):
        """
        Return the complete route with categories included
        """
        parts = [ c.slug for c in self.category.all() ]
        parts.append(self.slug)
        return "/".join(parts)

    @models.permalink
    def get_absolute_url(self):
        parts = [ c.slug for c in self.category.all() ]
        parts.append(self.slug)
        slug = "/".join(parts)
        return ('product-detail', [slug])

    def is_new(self):
        desde = datetime.datetime.today() - datetime.timedelta(days=7)
        return self.date_added >= desde

    @property
    def price(self):
        return self.unit_price

    @property
    def rating(self):
        obj = self.reviews.aggregate(Avg('rating'))
        return round(obj['rating__avg'])

    @property
    def reviews(self):
        content_type = ContentType.objects.get_for_model(self)
        return CommentWithRatings.objects.filter(content_type=content_type, object_pk=self.pk)

    @classmethod
    def get_by_slug(self, slug):
        return self.objects.get(absolute_url=slug)

    def get_images(self):
        return self.images.all()

    def save(self, *args, **kwargs):
        if (self.pk):
            self.absolute_url = self.get_absolute_slug()
        super(Product, self).save(*args, **kwargs)

    def has_specifications(self):
        return self.width or self.height or self.length or self.diameter or self.weight or self.capacity

    class Meta:
        ordering = ['-id', 'name']


class Image(models.Model):
    name = models.CharField(max_length=255)
    product = models.ForeignKey('Product', related_name='images')
    image = FilerImageField(null=True, blank=True)
    position = models.PositiveSmallIntegerField("position", blank=True, null=True)
    def __unicode__(self):
        return "%s" % self.name

class Attachment(models.Model):
    name = models.CharField(max_length=255)
    body = models.TextField(blank=True, verbose_name='Description')
    product = models.ForeignKey('Product', related_name='attachments')
    file = FilerFileField(null=True, blank=True)
    position = models.PositiveSmallIntegerField("position", blank=True, null=True)

    def __unicode__(self):
        return "%s" % self.name

class Tax(models.Model):
    name = models.CharField(max_length=255)
    value = models.FloatField()
    active = models.BooleanField(default=True)


class Order(models.Model):

    PROCESSING = 10  # New order, addresses and shipping/payment methods chosen (user is in the shipping backend)
    CONFIRMING = 20 # The order is pending confirmation (user is on the confirm view)
    CONFIRMED = 30 # The order was confirmed (user is in the payment backend)
    COMPLETED = 40 # Payment backend successfully completed
    SHIPPED = 50 # The order was shipped to client
    CANCELLED = 60 # The order was cancelled
    STATUS_CODES = (
        (PROCESSING, _('Processing')),
        (CONFIRMING, _('Confirming')),
        (CONFIRMED, _('Confirmed')),
        (COMPLETED, _('Completed')),
        (SHIPPED, _('Shipped')),
        (CANCELLED, _('Cancelled')),
    )
    user = models.OneToOneField(User, null=True, blank=True)
    status = models.IntegerField(choices=STATUS_CODES, default=PROCESSING,
                                 verbose_name=_('Status'))
    order_subtotal = CurrencyField(verbose_name=_('Order subtotal'))
    order_total = CurrencyField(verbose_name=_('Order Total'))
    shipping_address_text = models.TextField(_('Shipping address'), blank=True,
                                             null=True)
    billing_address_text = models.TextField(_('Billing address'), blank=True,
                                            null=True)


    shipping_method = models.ForeignKey('ShippingMethod', blank=True, null=True)
    
    cart = models.ForeignKey('Cart', blank=True, null=True)

    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    objects = OrderManager()

    def set_billing_address(self, billing_address):
        if  hasattr(billing_address, 'as_text'):
            self.billing_address_text = billing_address.as_text()
            self.save()

    def set_shipping_address(self, shipping_address):
        if hasattr(shipping_address, 'as_text'):
            self.shipping_address_text = shipping_address.as_text()
            self.save()
            
    def __unicode__(self):
        return "%s %s" % (self.date_created, self.user)

        
class OrderItem(models.Model):
    order = models.ForeignKey('Order', related_name='items',
                              verbose_name=_('Order'))
    
    name = models.CharField(_('Product name'), max_length=255)
    reference = models.CharField(_('Product referente'), max_length=255)
    unit_price = CurrencyField(verbose_name=_('Unit price'))
    quantity = models.IntegerField()
    
    product = models.ForeignKey('Product',
                                verbose_name=_('Product'), null=True, blank=True)
    @property
    def total(self):
        return self.quantity * self.unit_price
    

class Cart(models.Model):
    SESSION_CART_ID ='o2w_cart'
    user = models.OneToOneField(User, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    ip = models.CharField(max_length=255, null=True, blank=True)

    def add_product(self, product, quantity=1, merge=True):
        self.save()

        item = CartItem.objects.filter(cart=self, product=product)
        # Let's see if we already have an Item with the same product ID
        if item.exists() and merge:
            cart_item = item[0]
            cart_item.quantity = cart_item.quantity + int(quantity)
            cart_item.save()
        else:
            cart_item = CartItem.objects.create(
                cart=self, quantity=quantity, product=product)
            cart_item.save()

        return cart_item


    def delete_product(self, product):
        self.items.filter(product=product).delete()

    def delete_item(self, cart_item_id):
        cart_item = self.items.get(pk=cart_item_id)
        cart_item.delete()
        self.save()

    def update_item(self, cart_item_id, quantity):
        cart_item = self.items.get(pk=cart_item_id)
        cart_item.quantity = quantity
        cart_item.save()

    def empty(self):
        if self.pk:
            self.items.all().delete()
            self.delete()

    def get_items(self):
        return self.items.all()

        
    @property
    def total_quantity(self):
        """
        Returns the total quantity of all items in the cart
        """
        return sum([ci.quantity for ci in self.items.all()])

    @property
    def total(self):
        return sum([ci.total for ci in self.items.all()])

    @property
    def order(self):
        orders = self.order_set.all()
        if orders:
            return orders[0]
            
    @classmethod
    def get_from_request(self, request):
        cart = None
        cart_id = request.session.get(self.SESSION_CART_ID)
        if cart_id:
            try:
                cart = Cart.objects.get(pk=cart_id)
            except:
                pass

        if not cart:
            cart = Cart(ip = request.META['REMOTE_ADDR'])
            cart.save()
            request.session[self.SESSION_CART_ID] = cart.pk
        return cart

    @models.permalink
    def get_absolute_url(self):
        return ('cart', )

    def __unicode__(self):
        return "%s %s" % (self.id, self.date_created)
        
class CartItem(models.Model):
    cart = models.ForeignKey('Cart', related_name="items")
    quantity = models.IntegerField()
    product = models.ForeignKey('Product')

    @property
    def total(self):
        return self.quantity * self.product.price


class Country(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return u'%s' % self.name

    class Meta(object):
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')



ADDRESS_TEMPLATE = \
_("""
Name: %(name)s,
Address: %(address)s,
Zip-Code: %(zipcode)s,
City: %(city)s,
State: %(state)s,
Country: %(country)s
""")

class Address(models.Model):
    user_shipping = models.OneToOneField(User, related_name='shipping_address',
                                         blank=True, null=True)
    user_billing = models.OneToOneField(User, related_name='billing_address',
                                        blank=True, null=True)

    name = models.CharField(_('Name'), max_length=255)
    address = models.CharField(_('Address'), max_length=255)
    address2 = models.CharField(_('Address2'), max_length=255, blank=True)
    zip_code = models.CharField(_('Zip Code'), max_length=20)
    city = models.CharField(_('City'), max_length=20)
    state = models.CharField(_('State'), max_length=255)
    country = models.ForeignKey(Country, verbose_name=_('Country'), blank=True,
                                null=True)

    class Meta(object):
        verbose_name = _('Address')
        verbose_name_plural = _("Addresses")

    def __unicode__(self):
        return '%s (%s, %s)' % (self.name, self.zip_code, self.city)

    def clone(self):
        new_kwargs = dict([(fld.name, getattr(self, fld.name))
                           for fld in self._meta.fields if fld.name != 'id'])
        return self.__class__.objects.create(**new_kwargs)

    def as_text(self):
        return ADDRESS_TEMPLATE % {
            'name': self.name,
            'address': '%s\n%s' % (self.address, self.address2),
            'zipcode': self.zip_code,
            'city': self.city,
            'state': self.state,
            'country': self.country,
        }


class ShippingMethod(models.Model):
    name = models.CharField(_("Title"), max_length=125, help_text=_('Title of the shipping method'))
    active = models.BooleanField(default=True)
    text = models.TextField(_("Descriptión"))
    price = models.FloatField(_("Price"), help_text=_("Set the price if is not calculated"), blank=True, null=True)
    function = models.CharField(_("Module where the price is calculated"), blank=True, null=True, max_length=255)
    position = models.IntegerField(blank=True, null=True)
    image = models.ImageField(upload_to='shipping_method', blank=True)

    def __unicode__(self):
        return self.name


    class Meta:
        ordering = ['position']
