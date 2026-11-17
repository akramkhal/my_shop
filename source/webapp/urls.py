from django.urls import path
from webapp.views import (ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView,
                          ProductDeleteView, categories_view, category_add_view, category_edit_view,
                          category_delete_view, category_delete_view, CartAddView, CartView,
                          CartDeleteView, CartDecreaseView)

urlpatterns = [
    path('', ProductListView.as_view(), name='index'),
    path('products/', ProductListView.as_view(), name='products'),
    path('products/add/', ProductCreateView.as_view(), name='product_add'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_view'),
    path('products/<int:pk>/edit/', ProductUpdateView.as_view(), name='product_edit'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('categories/', categories_view, name='categories'),
    path('categories/add/', category_add_view, name='category_add'),
    path('categories/<int:pk>/edit/', category_edit_view, name='category_edit'),
    path('categories/<int:pk>/delete/', category_delete_view, name='category_delete'),
    path('products/<int:pk>/add-to-cart/', CartAddView.as_view(), name='cart_add'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/<int:pk>/delete/', CartDeleteView.as_view(), name='cart_delete'),
    path('cart/<int:pk>/decrease/', CartDecreaseView.as_view(), name='cart_decrease'),
]