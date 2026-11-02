from decimal import Decimal, InvalidOperation

from django.shortcuts import render, get_object_or_404, redirect
from webapp.models import Product, Category
from webapp.forms import ProductForm

def products_view(request):
    context = {
        'products': Product.objects.filter(stock__gt=0).order_by('category__name', 'name')
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
        form = ProductForm()
        return render(request, 'product_add.html', {'form': form})
    elif request.method == 'POST':
        form = ProductForm(data=request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            price = form.cleaned_data.get('price')
            image = form.cleaned_data.get('image')
            category = form.cleaned_data.get('category')
            description = form.cleaned_data.get('description')
            stock = form.cleaned_data.get('stock')
            product = Product.objects.create(name=name, price=price, image=image, category=category, description=description, stock=stock)
            return redirect('product_view', pk=product.pk)
        else:
            return render(request, 'product_add.html', {'form': form})


def product_edit_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'GET':
        form = ProductForm(initial={'name': product.name, 'price': product.price, 'image': product.image, 'category': product.category,
                                   'description': product.description, 'stock': product.stock})
        return render(request, 'product_edit.html', {'product': product, 'form': form})
    elif request.method == 'POST':
        form = ProductForm(data=request.POST)
        if form.is_valid():
            product.name = form.cleaned_data.get('name')
            product.price = form.cleaned_data.get('price')
            product.image = form.cleaned_data.get('image')
            product.category = form.cleaned_data.get('category')
            product.description = form.cleaned_data.get('description')
            product.stock = form.cleaned_data.get('stock')
            product.save()
            return redirect('product_view', pk=product.id)
        else:
            return render(request, 'product_edit.html', {'product': product, 'form': form})


def product_delete_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'GET':
        return render(request, 'delete_product.html', {'product': product})
    elif request.method == 'POST':
        product.delete()
        return redirect('products')


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
