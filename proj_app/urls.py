from django.views.generic import TemplateView
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('show/', TemplateView.as_view(template_name='home_page.html'), name='show'),
]