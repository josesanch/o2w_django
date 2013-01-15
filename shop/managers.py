from django.db import models

class OrderManager(models.Manager):
    
    def create_from_cart(self, cart):
        from o2w.shop.models import Order, OrderItem
        order = Order()
        order.cart = cart
        order.save()
        for item in cart.get_items():
            order_item = OrderItem()
            order_item.order = order
            order_item.product = item.product
            order_item.name = item.product.name
            order_item.reference = item.product.reference
            order_item.unit_price = item.product.price
            order_item.quantity = item.quantity
            order_item.save()
            
        return order
        
