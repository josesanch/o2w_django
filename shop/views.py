#encoding:utf-8
from o2w.shop import models, forms
from django.views import generic
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from pure_pagination.mixins import PaginationMixin
import datetime

class ShopView(generic.TemplateView):
    template_name = 'shop/index.html'


class CategoryListView(generic.ListView):
    model = models.Category

class ProductListView(PaginationMixin, generic.ListView):
    template_name = 'shop/list.html'
    model = models.Product

    paginate_by = 9

    def get_queryset(self):
        
        queryset = super(ProductListView, self).get_queryset()
        query = self.request.GET.get('query', None) or self.request.POST.get('query', None)
        type = self.request.GET.get('type', None) or self.request.POST.get('type', None)
        range = self.request.GET.get('range', None)  or self.request.POST.get('range', None)
        room = self.request.GET.get('room', None)  or self.request.POST.get('room', None)
        price = self.request.GET.get('price', None)  or self.request.POST.get('price', None)
        is_offer = self.request.GET.get('offer', None)  or self.request.POST.get('offer', None)
        is_new = self.request.GET.get('new', None)  or self.request.POST.get('new', None)
        sort_by = self.request.GET.get('sort_by', None)  or self.request.POST.get('sort_by', None)
        page_size = self.request.GET.get('page_size', None)  or self.request.POST.get('page_size', None)

        if query:
            queryset = queryset.filter(name__icontains=query)

        if room:
            rooms = room.split(",")
            categories = models.Category.objects.filter(parent__slug='room', slug__in=rooms)
            queryset = queryset.filter(category__in=categories)

        if type:
            types = type.split(",")
            categories = models.Category.objects.filter(parent__slug='type', slug__in=types)
            queryset = queryset.filter(category__in=categories)

        if range:
            ranges = range.split(",")
            categories = models.Category.objects.filter(parent__slug='range', slug__in=ranges)
            queryset = queryset.filter(category__in=categories)

        if is_new:
            desde = datetime.datetime.today() - datetime.timedelta(days=7)
            queryset = queryset.filter(date_added__gte=desde)

        if is_offer:
            queryset = queryset.filter(offer=True)

        if price:
            prices = price.split(",")
            q = Q()
            for p in prices:
                desde, hasta = p.split('-')
                if hasta:
                    q |= Q(unit_price__range=(desde, hasta))
                else:
                    q |= Q(unit_price__gte=desde)

            queryset = queryset.filter(q)

        if sort_by:
            queryset = queryset.order_by(sort_by)

        if page_size and page_size in ('18', '36') :
            self.paginate_by = int(page_size)
            
        queryset = queryset.distinct()

    
        return queryset


class ProductDetailView(generic.DetailView):
    model = models.Product
    
    def get_object(self):
        slug = self.kwargs['slug']
        return models.Product.get_by_slug(slug)


class CartView(generic.UpdateView):
    template_name = 'shop/cart.html'

    def get_object(self):
        return self.request.cart

    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        context.update({'page': 'cart'})
        return context



    def post(self, request, *args, **kwargs):
        cart = self.get_object()
        request = self.request
        action = request.POST.get("action")

        if action == 'add':
            product = get_object_or_404(models.Product, pk=request.POST.get('product'))
            cart.add_product(product, request.POST.get('quantity'))

        if action == 'remove':
            cart.delete_item(request.POST.get('item'))

        if action == 'update':
            item = get_object_or_404(models.Product, pk=request.POST.get('item'))
            cart.update_item(item, request.POST.get('quantity'))

        return super(CartView, self).post(self, request, *args, **kwargs)



class CheckoutView(generic.TemplateView):
    template_name = 'shop/checkout.html'

    def get_context_data(self, **kwargs):
        context = super(CheckoutView, self).get_context_data(**kwargs)
        billing_address = None
        shipping_address = None
        data = None
        if self.request.method == 'POST':
            data = self.request.POST

        if self.request.user:
            try:
                billing_address = self.request.user.billing_address
            except: pass

            try:
                shipping_address = self.request.user.shipping_address
            except: pass

        billing = forms.AddressForm(data, prefix="billing", instance=billing_address)
        shipping = forms.AddressForm(data, prefix="shipping", instance=shipping_address)

                
        context.update({
            'object': {
                'billing': billing,
                'shipping': shipping,
                'login': forms.UserForm(),
            },
            'page': 'checkout'
        })
        return context


    def post(self, request, *args, **kwargs):
        """
        Here we create the order in processing status
        """
        context = self.get_context_data(**kwargs)
        billing = context['object']['billing']
        shipping = context['object']['shipping']

        if billing.is_valid() and shipping.is_valid():
            billing_instance = billing.save(commit=False)
            shipping_instance = shipping.save(commit=False)

            billing_instance.user_billing = request.user
            shipping_instance.user_shipping = request.user

            billing = billing_instance.save()
            shipping = shipping_instance.save()

            order = models.Order.objects.create_from_cart(self.request.cart)
            order.set_billing_address(billing)
            order.set_shipping_address(shipping)
            order.user = self.request.user
            order.save()
            
            return redirect('shipping')
        return self.render_to_response(context)



class ShippingView(generic.TemplateView):
    template_name = 'shop/shipping.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        order = self.request.cart.order
        order.shipping_method_id = self.request.POST.get('shipping', None)
        order.save()
        return redirect('summary')
    #//        return self.render_to_response(context)
        
    def get_context_data(self, **kwargs):
        context = super(ShippingView, self).get_context_data(**kwargs)
        shippings = models.ShippingMethod.objects.filter(active=True)
        context.update({ 'object_list': shippings, 'page': "shipping" })
        return context
    


        
class SummaryView(generic.TemplateView):
    """
    Here we:
    * create the order 
    * apply the custom shipping method
    * Show a summary and process payment
    """
    template_name = 'shop/summary.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        
        return self.render_to_response(context)
        
    def get_context_data(self, **kwargs):
        context = super(SummaryView, self).get_context_data(**kwargs)
        shippings = models.ShippingMethod.objects.filter(active=True)
        context.update({
            'page': 'summary',
            'cart': self.request.cart,
        })
        return context
    

class PaymentView(generic.TemplateView):
    template_name = 'shop/payment.html'

