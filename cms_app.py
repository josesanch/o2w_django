from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

class ShopApp(CMSApp):
    name = _("Shop app") # give your app a name, this is required
    urls = ["o2w.shop.urls"] # link your app to url configuration(s)

apphook_pool.register(ShopApp) # register your app

