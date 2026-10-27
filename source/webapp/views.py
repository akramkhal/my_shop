from decimal import Decimal, InvalidOperation

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
        return redirect('categories')


def product_add_view(request):
    if request.method == 'GET':
        return render(request, 'product_add.html', {'categories': Category.objects.all()})
    elif request.method == 'POST':
        name = request.POST.get('name', "").strip()
        price = request.POST.get('price', "").strip()
        image = request.POST.get('image', "").strip()
        category = request.POST.get('category', "").strip()
        description = request.POST.get('description', "").strip()

        errors = []
        if not name:
            errors.append("Название обязательно!")
        if not image:
            errors.append("Ссылка на изображение обязательна!")
        if price:
            try:
                value = Decimal(price)
            except InvalidOperation:
                errors.append("Неверная цена!")
            else:
                if  value <= 0:
                    errors.append("Неверная цена!")
        else:
            errors.append("Цена обязательна!")
        if not category.isdigit() or not Category.objects.filter(pk=category).exists():
            errors.append("Выберите категорию!")

        if errors:
            context = {
                'name': name,
                'image': image,
                'price': price,
                'description': description or "",
                'category': category,
                'categories': Category.objects.all(),
                'errors': errors}
            return render(request, 'product_add.html', context)

        product = Product.objects.create(name=name, image=image, price=price, description=description, category_id=category)
        return redirect('product_view', pk=product.pk)


def categories_view(request):
    categories = Category.objects.all().order_by('name')
    return render(request, 'categories.html', {'categories': categories})


def category_delete_view(request, pk):
    if request.method == 'POST':
        category = get_object_or_404(Category, pk=pk)
        category.delete()
    return redirect('categories')

def category_edit_view(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'GET':
        context = {
            'category': category,
            'name': category.name,
            'description': category.description or "",
        }
        return render(request, 'category_edit.html', context)
    elif request.method == 'POST':
        name = request.POST.get('name', "").strip()
        description = request.POST.get('description', "").strip()

        errors = []
        if not name:
            errors.append("Название обязательно!")
        elif Category.objects.filter(name=name).exclude(pk=category.pk).exists():
            errors.append("Такая категория уже существует!")

        if errors:
            context = {
                'category': category,
                'name': name,
                'description': description,
                'errors': errors,
            }
            return render(request, 'category_edit.html', context)

        category.name = name
        category.description = description
        category.save()
        return redirect('categories')
