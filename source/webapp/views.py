from django.shortcuts import render, get_object_or_404, redirect
from webapp.models import Product, Category

def products_view(request):
    context = {
        'products': Product.objects.all().order_by('-created_at')
    }
    return render(request, 'products.html', context)


def product_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_view.html', {'product': product})


def category_add_view(request):
    if request.method == 'GET':
        return render(request, 'category_add.html')
    elif request.method == 'POST':
        name = request.POST.get('name', "").strip()
        description = request.POST.get('description', "").strip()

        errors = []
        if not name:
            errors.append("Название обязательно!")
        elif Category.objects.filter(name=name).exists():
            errors.append("Такая категория уже существует!")

        if errors:
            context = {
                'name': name,
                'description': description or "",
                'errors': errors}
            return render(request, 'category_add.html', context)
        Category.objects.create(name=name, description=description)
        return redirect('index')

