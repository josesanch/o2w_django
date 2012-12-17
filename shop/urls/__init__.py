from django.conf.urls import patterns, url
import views

urlpatterns = patterns(
    '',
    url(r'^/$', 'root', name='shop'),
    url(r'^/cart/$', 'cart', name='cart'),
    url(r'^/checkout/$', 'checkout', name='checkout'),
    url(r'^/orders/$', 'orders', name='orders'),
    url(r'^/search/$', 'search', views.ProductListView.as_view(), name='search'),
    url(r'^/(?P<slug>[^/]*)/$', 'category', views.CategoryListView.as_view(), name='category'),
    url(r'^(?P<slug>[0-9A-Za-z-_.//]+)/$', views.ProductDetailView.as_view(), name='product-detail'),
)
