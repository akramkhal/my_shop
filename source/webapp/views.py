from django.shortcuts import render
from webapp.models import Product, Category

def products_view(request):
    context = {
        'products': Product.objects.all().order_by('-created_at')
    }
    return render(request, 'products.html', context)
