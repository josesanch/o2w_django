import models

class CartMiddleware(object):
    def process_request(self, request):        
        request.cart = models.Cart().get_from_request(request)
