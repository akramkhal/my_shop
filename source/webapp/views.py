from django.shortcuts import render, get_object_or_404
from webapp.models import Product, Category

def products_view(request):
    context = {
        'products': Product.objects.all().order_by('-created_at')
    }
    return render(request, 'products.html', context)

def product_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_view.html', {'product': product})
