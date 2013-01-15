from django.conf.urls import patterns, url
from o2w.shop import views
from django.contrib.auth.decorators import login_required



login_url = '/user/login/'
urlpatterns = patterns(
    '',
    url(r'^$', views.ShopView.as_view(), name='shop'),
    url(r'^cart/$', views.CartView.as_view(), name='cart'),
    url(r'^checkout/$', login_required(views.CheckoutView.as_view(), login_url=login_url), name='checkout'),
    url(r'^shipping/$', login_required(views.ShippingView.as_view(), login_url=login_url), name='shipping'),
    url(r'^summary/$', login_required(views.SummaryView.as_view(), login_url=login_url), name='summary'),
    url(r'^payment/$', login_required(views.PaymentView.as_view(), login_url=login_url), name='payment'),
    #    url(r'^orders/$', login_required('orders', name='orders'),

    url(r'^search/$', views.ProductListView.as_view(), name='search'),
    url(r'^(?P<slug>[^/]*)/$', 'category', views.CategoryListView.as_view(), name='category'),
    url(r'^(?P<slug>[0-9A-Za-z-_.//]+)/$', views.ProductDetailView.as_view(), name='product-detail'),
)
