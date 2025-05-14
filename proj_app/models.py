from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    id_name = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.jpeg')
    bio = models.TextField(max_length=500, blank=True, default='')
    location = models.CharField(max_length=30, blank=True, default='')
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='custom_user',
                                null = True,  # 允许空值
                                blank = True
                                )


class UserGoodsItem(models.Model):
    title = models.CharField(max_length=100)
    simple_description = models.TextField(default=" ")
    image = models.ImageField(upload_to='uploads/')
    description = models.TextField(default=" ")  # 新增详细描述字段
    from_location = models.CharField(max_length=100)
    goods_price = models.FloatField(default=0.00)
    origin_price = models.FloatField(default=0.00)
    goods_rest_num = models.IntegerField(default=0)
    goods_sale_num = models.IntegerField(default=0)
    inserter = models.CharField(max_length=100, default='')
    inserter_name = models.CharField(max_length=100, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# 购物车
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # 每个用户对应一个购物车
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)  # 购物车条目属于某个购物车
    product = models.ForeignKey(UserGoodsItem, on_delete=models.CASCADE)  # 条目关联商品
    quantity = models.PositiveIntegerField(default=1)  # 商品数量
    added_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return self.product.goods_price * self.quantity

# 订单
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    custom_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total_price = models.FloatField(default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='seller_orders',
        null=True  # 允许空值保证迁移兼容性
    )
    STATUS_CHOICES = [
        ('P', '已支付'),
        ('S', '已发货'),
        ('C', '已完成'),
    ]
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_item_set')
    product = models.ForeignKey(UserGoodsItem, on_delete=models.CASCADE)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    custom_seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.FloatField(default=0.00)
    all_price = models.FloatField(default=0.00)
    note = models.TextField(default='')

# 评论区系统
class Review(models.Model):
    product = models.ForeignKey(UserGoodsItem, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    custom_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])  # 1-5分
    comment = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'user')  # 每个用户只能评价一次

# 会话栏
class Conversation(models.Model):
    participant1 = models.ForeignKey(User, related_name='conversations1', on_delete=models.CASCADE)
    participant2 = models.ForeignKey(User, related_name='conversations2', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [['participant1', 'participant2']]

# 对话
class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    sender_custom_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


