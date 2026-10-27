from django.urls import path
from webapp.views import (products_view, product_view, category_add_view, product_add_view,
                          categories_view)

urlpatterns = [
    path('', products_view, name='index'),
    path('products/', products_view, name='products'),
    path('products/<int:pk>/', product_view, name='product_view'),
    path('categories/add/', category_add_view, name='category_add'),
    path('products/add/', product_add_view, name='product_add'),
    path('categories/', categories_view, name='categories'),
]
