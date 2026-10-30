from django.contrib import admin
from webapp.models import Product, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'image', 'category', 'description', 'stock')
    list_filter = ('category',)
    search_fields = ('name',)
