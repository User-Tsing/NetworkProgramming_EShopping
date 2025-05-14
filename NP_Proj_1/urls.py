"""
URL configuration for NP_Proj_1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from proj_app import views
from django.contrib.auth import views as auth_views

urlpatterns = [
       path('admin/', admin.site.urls),
       path('', views.home),
       path('register/', views.register_view, name='register'),
       path('login/', views.login_view, name='login'),
       path('detail/<int:item_id>/', views.detail_view, name='detail'),
       path('upload_goods/', views.upload_goods, name='upload_goods'),
       path('main/', views.user_main, name='user_main'),
       path('checkout/', views.checkout_view, name='checkout'),
       path('confirm-payment/', views.confirm_payment, name='confirm_payment'),
       path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
       path('search/', views.search_view, name='search_view'),
       path('bought_history/', views.order_view, name='order_view'),
       path('goods_sale/', views.goods_sale_view, name='goods_sale_view'),
       path('update_profile/', views.update_profile, name='update_profile'),
       path('main_land/<str:username>/', views.main_land, name='main_land'),
       path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
       path('chats/', views.ChatListView.as_view(), name='chat_list'),
       path('chats/<int:user_id>/', views.ChatRoomView.as_view(), name='chat_room'),
       path('send_message/', views.send_message, name='send_message'),
       path('update_goods/<int:goods_id>/', views.update_goods, name='update_goods'),
       path('check_order/<int:order_id>', views.check_order, name='check_order'),
       path('user_check_order/<int:order_id>/', views.user_check_order, name='user_check_order'),
       path('update_cart_item_quantity/<int:item_id>/', views.update_cart_item_quantity, name='update_cart_item_quantity'),
       path('delete_cart_item/<int:item_id>/', views.delete_cart_item, name='delete_cart_item'),
       path('delete_selected_cart_items/', views.delete_selected_cart_items, name='delete_selected_cart_items'),
       path('developer_show/', views.developer_show, name='developer_show'),
       path('detail_json/<int:goods_id>/', views.get_goods_json, name='detail_json'),
       path('app_include/', include('proj_app.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
