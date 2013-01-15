#encoding:utf-8
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.db.models import ManyToManyField
from django.forms import CheckboxSelectMultiple, CheckboxInput
from django.utils.encoding import force_unicode
from django.utils.html import conditional_escape
from itertools import chain
import models

from django.utils.safestring import mark_safe

class CategoryAdmin(ModelAdmin):
    list_display = ('pk', 'name', 'parent', 'active')
    prepopulated_fields = {"slug": ("name",)}

class ImageInline(admin.TabularInline):
    model = models.Image
    extra = 1

class AttachmentInline(admin.TabularInline):
    model = models.Attachment
    extra = 0

class ProductForm(forms.ModelForm):

    # categories = MPTTModelMultipleChoiceField(
    #                 ProductCategory.objects.all(),
    #                 widget = MPTTFilteredSelectMultiple("Categories",False,attrs={'rows':'10'})
    #             )

    category = CheckboxSelectMultiple()
    class Meta:
        model = models.Product



class CategoryCheckbox(CheckboxSelectMultiple):
    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = []
        final_attrs = self.build_attrs(attrs, name=name)
        output = [u'<ul>']
        output.append(self.__render_childs(name, value, final_attrs, None))
        output.append(u'</ul>')
        return mark_safe(u'\n'.join(output))

    def __render_childs(self, name, str_values, final_attrs, parent):
        output = [u'<ul>']
        categories = models.Category.objects.filter(parent=parent)
        for category in categories:
            rendered_cb = CheckboxInput(final_attrs, check_test=lambda value: value in str_values).render(name, category.pk)

            output.append(u'<li><label>%s %s</label></li>' % (rendered_cb, category.name))
            output.append(self.__render_childs(name, str_values, final_attrs, category))


        output.append(u'</ul>')
        return mark_safe(u'\n'.join(output))


class ProductAdmin(ModelAdmin):
    #    form = ProductForm
    def queryset(self, request):
        # use our manager, rather than the default one
        qs = self.model.includeinactive.get_query_set()

        # we need this from the superclass method
        ordering = self.ordering or () # otherwise we might try to *None, which is bad ;)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs
    list_editable = ('active', 'unit_price')
    list_display = ('name', 'reference',  'active', 'unit_price', 'absolute_url')
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ('category', )
    inlines = [ImageInline, AttachmentInline ]

    fieldsets = (
        (None, {
            'fields': (

            )
        }),
        (None, {
            'fields': (
                ('name', 'slug'),
                ('unit_price', 'reference'),
                ('body'),
                ('image'),
                ('active', 'offer'),
                ('category', 'taxes'),
            )
        }),
        (_('Size/weight/capacity'), {
            'classes': ('collapse',),
            'fields': (
                ('height', 'length', 'width',),
                ('weight', 'capacity', 'diameter'),
            )
        }),

    )

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "category":
            kwargs['widget'] = CategoryCheckbox

        return super(ProductAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def response_add(self, request, new_object):
        new_object.save()
        return super(ProductAdmin, self).response_add(request, new_object)

    def response_change(self, request, obj):
        obj.save()
        return super(ProductAdmin, self).response_change(request, obj)

class AddressAdmin(ModelAdmin):
    list_display = ('__unicode__', 'user_shipping', 'user_billing')

class ShippingAdmin(ModelAdmin):
    list_display = ('__unicode__', 'price', 'active')


class OrderAdmin(ModelAdmin):
    pass
    
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Tax)
admin.site.register(models.Country)
admin.site.register(models.Address, AddressAdmin)
admin.site.register(models.ShippingMethod, ShippingAdmin)
admin.site.register(models.Order, OrderAdmin)
