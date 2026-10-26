from django.urls import path
from webapp.views import products_view, product_view

urlpatterns = [
    path('', products_view, name='index'),
    path('products/', products_view, name='products'),
    path('products/<int:pk>/', product_view, name='product_view'),
]
