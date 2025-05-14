from django.contrib import admin

# Register your models here.

from .models import UserGoodsItem, CustomUser, CartItem, Cart, Order, OrderItem, Review, Conversation, Message

admin.site.register(UserGoodsItem)  # 注册模型
admin.site.register(CustomUser)
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Review)
admin.site.register(Conversation)
admin.site.register(Message)


