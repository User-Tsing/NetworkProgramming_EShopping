from datetime import timezone
import datetime

from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.db import transaction
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.generic import ListView, DetailView
from django.db import models

# Create your views here.

import json
from .models import UserGoodsItem, CustomUser, CartItem, Cart, OrderItem, Order, Review, Conversation, Message

# 初始界面渲染和请求处理
# 主界面
def home(request, user=None):
    if request.method == "POST":
        if request.POST.get("transfer_to") == "login":
            return JsonResponse({'redirect': '/login/'})
    # items = UserGoodsItem.objects.all().order_by('-created_at')  # 获取表单全部内容
    items = UserGoodsItem.objects.all().order_by('-goods_sale_num')  # 获取表单全部内容
    if request.user.is_authenticated:
        user = get_object_or_404(CustomUser, username=request.user.username)
        has_unread_messages = False
        unread_messages_1 = Message.objects.filter(
            conversation__participant1=request.user,
            is_read=False
        )
        for unread_message in unread_messages_1:
            if unread_message.conversation.participant2 == unread_message.sender:
                has_unread_messages = True
        unread_messages_2 = Message.objects.filter(
            conversation__participant2=request.user,
            is_read=False
        )
        for unread_message in unread_messages_2:
            if unread_message.conversation.participant1 == unread_message.sender:
                has_unread_messages = True
    else:
        has_unread_messages = False
    query = request.GET.get('q', '')
    if query:
        items = items.filter(
            Q(title__icontains=query) |
            Q(simple_description__icontains=query)
        )
        return render(request, 'search.html', {'items': items, 'query': query, 'user': user})
    return render(request, 'home.html', {'items': items, 'user': user, 'has_unread_messages': has_unread_messages})  # 全部导入




# 登录函数
def login_view(request):  # 登录处理
    if request.method == 'POST':
        username = request.POST.get('username')  # 读取表单
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)  # django函数处理登录数据
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True, 'redirect': '/'})  # 返回重定向地址：首页
        return JsonResponse({'success': False, 'error': 'Invalid credentials'})  # 返回错误信息
    return render(request, 'login.html')  # 界面打开函数：打开界面（打开界面是GET）


# 注册函数
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        id_name = request.POST.get('id_name')

        # 验证逻辑
        if not all([username, email, password1, password2]):
            return JsonResponse({'success': False, 'error': 'All fields are required'})

        if password1 != password2:
            return JsonResponse({'success': False, 'error': 'Passwords do not match'})

        if User.objects.filter(username=username).exists():
            return JsonResponse({'success': False, 'error': 'Username already exists'})

        # 创建用户
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )
        CustomUser.objects.create(
            username=username,
            email=email,
            id_name=id_name,
            user=user
        )
        Cart.objects.create(
            user=user,
            created_at=datetime.datetime.now(),
        )
        print("finished")
        # login(request, user)  # 可选：注册后自动登录
        return JsonResponse({'success': True, 'redirect': '/'})

    # return JsonResponse({'success': False, 'error': 'Invalid request'})
    return render(request, 'register.html')

# 详情函数
def detail_view(request, item_id, user=None):
    item = get_object_or_404(UserGoodsItem, pk=item_id)
    items = UserGoodsItem.objects.all().order_by('-created_at')
    if request.user.is_authenticated:
        user = get_object_or_404(CustomUser, username=request.user.username)
    query = request.GET.get('q', '')
    if query:
        items = items.filter(
            Q(title__icontains=query) |
            Q(simple_description__icontains=query)
        )
        return render(request, 'search.html', {'items': items, 'query': query, 'user': user})
    # 检查用户是否购买过该商品
    can_review = False
    if request.user.is_authenticated:
        has_purchased = OrderItem.objects.filter(
            product=item,
            order__user=request.user
        ).exists()
        can_review = has_purchased and not Review.objects.filter(product=item, user=request.user).exists()

    # 处理评价提交
    if request.method == 'POST' and 'submit_review' in request.POST:
        if not can_review:
            return JsonResponse({'success': False, 'error': '无评价权限'})

        rating = int(request.POST.get('rating'))
        comment = request.POST.get('comment', '')

        Review.objects.create(
            product=item,
            user=request.user,
            custom_user=user,
            rating=rating,
            comment=comment
        )
        # return JsonResponse({'success': True})
    reviews = Review.objects.filter(product=item).select_related('user')

    return render(request, 'detail.html', {
        'item': item,
        'user': user,
        'reviews': reviews,
        'can_review': can_review
    })

# 上传商品
# @csrf_exempt
def upload_goods(request, user=None):
    if request.method == 'POST':
        # 1. 验证用户Token
        if request.user.is_authenticated:
            print("用户已登录")
            user = get_object_or_404(CustomUser, username=request.user.username)
            UserGoodsItem.objects.create(
                inserter=user.username,
                inserter_name=user.id_name,
                title=request.POST.get('title'),
                description=request.POST.get('description'),
                goods_price=request.POST.get('goods_price'),
                origin_price=request.POST.get('origin_price'),
                goods_rest_num=request.POST.get('goods_rest_num'),
                goods_sale_num=0,
                from_location=request.POST.get('from_location'),
                simple_description=request.POST.get('simple_description'),
                image=request.FILES['image']
            )
            # 2. 处理表单数据
            # 3. 保存到UserGoodsItem模型
            # 4. 返回JSON响应
            return JsonResponse({'status': 'success'})
        print("出错：未登录")
        return JsonResponse({'status': 'error'})
    if request.user.is_authenticated:
        user = get_object_or_404(CustomUser, username=request.user.username)
    return render(request, 'upload.html', {'user': user})
    # return JsonResponse({'error': 'Invalid method'}, status=405)

# 个人主页
def user_main(request):
    if request.user.is_authenticated:
        user = get_object_or_404(CustomUser, username=request.user.username)  # 找到对应的用户
        if request.method == 'POST':
            data = json.loads(request.body)
            selected_ids = data.get('selected_ids', [])
            cart_items = CartItem.objects.filter(
                id__in=selected_ids,
                cart__user=request.user
            )
            total = sum(item.total_price() for item in cart_items)
            return JsonResponse({'success': True, 'total': total})
        cart = Cart.objects.get_or_create(user=request.user)[0]
        cart_items = CartItem.objects.filter(cart=cart).select_related('product').order_by('-added_at')
        # cart_items = CartItem.objects.filter(cart=cart).select_related('product')
        if cart_items:
            print("Get it.")
            print(cart_items)
        return render(request, 'user_main.html', {'user': user, 'cart_items': cart_items})
    return render(request, 'user_main.html', {'user': None})

# 结算界面
def checkout_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # 获取选中商品ID
    selected_ids = request.GET.get('items', '').split(',')
    selected_ids = [int(id) for id in selected_ids if id]

    # 查询购物车项
    cart_items = CartItem.objects.filter(
        id__in=selected_ids,
        cart__user=request.user
    ).select_related('product')

    # 计算总价
    total = sum(item.total_price() for item in cart_items)

    return render(request, 'checkout.html', {
        'order_items': cart_items,
        'total_price': total
    })

# 账单支付界面
@require_POST
def confirm_payment(request):
    try:
        user = get_object_or_404(CustomUser, username=request.user.username)
        data = json.loads(request.body)
        selected_ids = data.get('items', [])
        notes = data.get('notes', {})
        print(notes)

        with transaction.atomic():
            # 获取购物车项并锁定库存
            cart_items = CartItem.objects.filter(
                id__in=selected_ids,
                cart__user=request.user
            ).select_related('product').select_for_update()

            # 按卖家分组
            seller_groups = {}
            for item in cart_items:
                seller = item.product.inserter  # 假设inserter字段存储卖家用户名
                if seller not in seller_groups:
                    seller_groups[seller] = []
                seller_groups[seller].append(item)

            # 为每个卖家创建独立订单
            created_orders = []
            for seller, items in seller_groups.items():
                # 计算当前卖家的总金额
                seller_total = sum(item.total_price() for item in items)
                print("seller_total", seller_total)

                # 创建订单
                order = Order.objects.create(
                    user=request.user,
                    total_price=seller_total,
                    custom_user=user,
                    status='P'  # 支付状态
                )
                created_orders.append(order.id)

                # 创建订单项
                for item in items:
                    product = item.product
                    # 扣减库存
                    if product.goods_rest_num < item.quantity:
                        raise Exception(f'商品 {product.title} 库存不足')

                    product.goods_rest_num -= item.quantity
                    product.goods_sale_num += item.quantity
                    product.save()

                    # 获取卖家用户实例
                    seller_user = User.objects.get(username=seller)
                    custom_seller = CustomUser.objects.get(username=seller)
                    print('seller_user', seller_user)

                    note = notes.get(str(item.id), '')
                    print('note', note)

                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        seller=seller_user,
                        custom_seller=custom_seller,
                        quantity=item.quantity,
                        price=product.goods_price,
                        all_price=product.goods_price * item.quantity,
                        note=note
                    )
                    Order.objects.filter(id=order.id).update(seller=seller_user)
                    print("order:over")

                # 删除已处理的购物车项
                CartItem.objects.filter(id__in=[item.id for item in items]).delete()

            return JsonResponse({
                'success': True,
                'order_ids': created_orders  # 返回所有创建的订单ID
            })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# 订单界面
@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        # 获取商品和用户购物车
        product = get_object_or_404(UserGoodsItem, id=product_id)
        cart, _ = Cart.objects.get_or_create(user=request.user)

        # 验证库存
        quantity = int(request.POST.get('quantity', 1))
        if product.goods_rest_num < quantity:
            return JsonResponse({
                'success': False,
                'error': f'库存不足，剩余{product.goods_rest_num}件'
            })

        # 创建或更新购物车项
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            # 如果已存在则增加数量
            cart_item.quantity += quantity
            cart_item.save()

        return JsonResponse({
            'success': True,
            'message': f'成功添加{quantity}件商品到购物车'
        })
    return JsonResponse({'success': False, 'error': '无效请求'})

# 搜索
def search_view(request):
    query = request.GET.get('q', '')
    items = UserGoodsItem.objects.all().order_by('-created_at')

    if query:
        items = items.filter(
            Q(title__icontains=query) |
            Q(simple_description__icontains=query)
        )

    return render(request, 'search.html', {
        'items': items,
        'query': query,
        'user': request.user.custom_user if request.user.is_authenticated else None
    })

# 订单
def order_view(request):
    if request.user.is_authenticated:
        user = get_object_or_404(CustomUser, username=request.user.username)  # 找到对应的用户
        orders = Order.objects.filter(user=request.user).prefetch_related('order_item_set').order_by('-created_at')
        return render(request, 'order_view.html', {'user': user, 'orders': orders})


def goods_sale_view(request):
    if request.user.is_authenticated:
        user = get_object_or_404(CustomUser, username=request.user.username)
        goods = UserGoodsItem.objects.filter(inserter=user.username).order_by('-created_at')

        # 获取所有包含用户商品的订单
        orders = Order.objects.filter(
            order_item_set__product__inserter=user.username
        ).prefetch_related('order_item_set__product').distinct().order_by('-created_at')

        return render(request, 'goods_sale_view.html', {
            'user': user,
            'goods': goods,
            'orders': orders  # 现在传递的是Order对象列表
        })
# 换头像
@login_required
@require_POST
def update_profile(request):
    user = get_object_or_404(CustomUser, username=request.user.username)
    if len(request.POST.get('id_name', '')) > 20:
        return JsonResponse({'success': False, 'error': '名称过长（最多20字）'})

    try:
        # 更新头像
        if 'avatar' in request.FILES:
            user.avatar = request.FILES['avatar']

        # 更新文本字段
        user.id_name = request.POST.get('id_name', user.id_name)
        user.bio = request.POST.get('bio', user.bio)
        user.location = request.POST.get('location', user.location)
        user.save()

        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

# 其他人界面
def main_land(request, username):
    user = get_object_or_404(CustomUser, username=username)
    if request.user.is_authenticated:
        customer = get_object_or_404(CustomUser, username=request.user.username)
        goods = UserGoodsItem.objects.filter(inserter=user.username).order_by('-created_at')
        return render(request, 'main_land.html', {'user': user, 'customer': customer, 'goods': goods})
    else:
        goods = UserGoodsItem.objects.filter(inserter=user.username).order_by('-created_at')
        return render(request, 'main_land.html', {'user': user, 'customer': None, 'goods': goods})


# 会话区
class ChatListView(ListView):
    template_name = 'chat_list.html'
    context_object_name = 'conversations'

    def get_queryset(self):
        conversations = Conversation.objects.filter(
            Q(participant1=self.request.user) |
            Q(participant2=self.request.user)
        ).order_by('-updated_at')

        # 为每个会话计算对方用户
        for conv in conversations:
            # conv.other_user = (
            #     conv.participant2
            #     if conv.participant1 == self.request.user
            #     else conv.participant1
            # )
            if conv.participant1 == self.request.user:
                conv.other_user = conv.participant2
            else:
                conv.other_user = conv.participant1
            conv.other_user = CustomUser.objects.get(username=conv.other_user.username)
            # 查询未读消息数量
            unread_count = Message.objects.filter(
                conversation=conv,
                sender=conv.other_user.user,
                is_read=False
            ).count()
            conv.unread_count = unread_count
        return conversations


class ChatRoomView(DetailView):
    template_name = 'chat_room.html'

    def get_object(self):
        user_id = self.kwargs['user_id']
        other_user = get_object_or_404(User, id=user_id)

        # 构造查询条件
        lookup = (
                Q(participant1=self.request.user, participant2=other_user) |
                Q(participant1=other_user, participant2=self.request.user)
        )

        # 手动查询和创建
        try:
            conversation = Conversation.objects.get(lookup)
        except Conversation.DoesNotExist:
            conversation = Conversation.objects.create(
                participant1=self.request.user,
                participant2=other_user
            )
        if conversation.participant1 == self.request.user:
            conversation.other_user = conversation.participant2
        else:
            conversation.other_user = conversation.participant1
        conversation.other_user = CustomUser.objects.get(username=conversation.other_user.username)

        Message.objects.filter(
            conversation=conversation,
            sender=conversation.other_user.user,
            is_read=False
        ).update(is_read=True)

        return conversation

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = self.object.messages.all().order_by('timestamp')
        context[
            'other_user'] = self.object.participant2 if self.object.participant1 == self.request.user else self.object.participant1
        return context


def send_message(request):
    if request.method == 'POST':
        receiver_id = request.POST.get('receiver_id')
        content = request.POST.get('content')
        receiver = get_object_or_404(User, id=receiver_id)
        custom_user = get_object_or_404(CustomUser, username=request.user.username)

        # 获取或创建对话
        conversation = Conversation.objects.filter(
            models.Q(participant1=request.user, participant2=receiver) |
            models.Q(participant1=receiver, participant2=request.user)
        ).first()

        if not conversation:
            conversation = Conversation.objects.create(
                participant1=request.user,
                participant2=receiver
            )

        Message.objects.create(
            conversation=conversation,
            sender=request.user,
            content=content,
            sender_custom_user=custom_user
        )
        return JsonResponse({'status': 'success'})

# 商品操作
@login_required
@require_POST
def update_goods(request, goods_id):
    goods = get_object_or_404(UserGoodsItem, id=goods_id)

    # 验证权限：当前用户必须是商品发布者
    if goods.inserter != request.user.username:
        return JsonResponse({'success': False, 'error': '无操作权限'})

    try:
        # 更新文本字段
        goods.title = request.POST.get('title', goods.title)
        goods.simple_description = request.POST.get('simple_description', goods.simple_description)
        goods.description = request.POST.get('description', goods.description)
        goods.goods_price = float(request.POST.get('price', goods.goods_price))
        goods.origin_price = float(request.POST.get('origin_price', goods.origin_price))
        goods.goods_rest_num = int(request.POST.get('stock', goods.goods_rest_num))
        goods.from_location = request.POST.get('from_location', goods.from_location)

        # 更新图片
        if 'image' in request.FILES:
            goods.image = request.FILES['image']

        goods.save()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def check_order(request, order_id):
    if request.method == 'POST':
        print(request.user.username)
        order_it = Order.objects.get(id=order_id)
        if request.user.username == order_it.seller.username:
            Order.objects.filter(id=order_id).update(
                status='S',
            )
            return render(request, 'check_order.html')

def user_check_order(request, order_id):
    if request.method == 'POST':
        print(request.user.username)
        order_it = Order.objects.get(id=order_id)
        if request.user.username == order_it.seller.username:
            Order.objects.filter(id=order_id).update(
                status='C',
            )
            return render(request, 'user_check_order.html')

# 购物车商品数量修改
@login_required
def update_cart_item_quantity(request, item_id):
    if request.method == 'POST':
        try:
            cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
            # 使用 json.loads 解析请求体
            data = json.loads(request.body)
            quantity = data.get('quantity')
            if quantity is not None and quantity > 0:
                product = cart_item.product
                if product.goods_rest_num >= quantity:
                    cart_item.quantity = quantity
                    cart_item.save()
                    return JsonResponse({'success': True})
                else:
                    return JsonResponse({'success': False, 'error': '库存不足'})
            else:
                return JsonResponse({'success': False, 'error': '无效的数量'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': '无效请求'})

# 删除购物车里的商品
@login_required
def delete_cart_item(request, item_id):
    if request.method == 'POST':
        try:
            cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
            cart_item.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': '无效请求'})

@login_required
def delete_selected_cart_items(request):
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body)
            selected_ids = data.get('selected_ids', [])
            cart_items = CartItem.objects.filter(
                id__in=selected_ids,
                cart__user=request.user
            )
            cart_items.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': '无效请求'})

# 开发者
def developer_show(request):
    return render(request, 'developer_show.html')


def get_goods_json(request, goods_id):
    try:
        good = UserGoodsItem.objects.get(id=goods_id)
        data = {
            'title': good.title,
            'simple_description': good.simple_description,
            'description': good.description,
            'goods_price': good.goods_price,
            'origin_price': good.origin_price,  # 确保这个字段存在于模型中
            'goods_rest_num': good.goods_rest_num,
            'from_location': good.from_location
        }
        print(good.origin_price)
        return JsonResponse(data)
    except UserGoodsItem.DoesNotExist:
        return JsonResponse({'error': '商品不存在'}, status=404)
