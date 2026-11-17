from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.http import urlencode, url_has_allowed_host_and_scheme
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View, TemplateView

from webapp.forms import ProductForm, SearchForm
from webapp.models import Product, Category, CartItem


class ProductListView(ListView):
    template_name = 'products.html'
    context_object_name = 'products'
    paginate_by = 5
    paginate_orphans = 1

    def get(self, request, *args, **kwargs):
        self.form = SearchForm(self.request.GET)
        self.search_value = None
        if self.form.is_valid():
            self.search_value = self.form.cleaned_data.get('search')
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Product.objects.filter(stock__gte=1).order_by('category__name', 'name')
        if self.search_value:
            queryset = queryset.filter(
                Q(name__icontains=self.search_value) |
                Q(description__icontains=self.search_value)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = self.form
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_view.html'


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_add.html'

    def get_success_url(self):
        return reverse('product_view', kwargs={'pk': self.object.pk})


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_edit.html'

    def get_success_url(self):
        return reverse('product_view', kwargs={'pk': self.object.pk})


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'delete_product.html'
    success_url = reverse_lazy('products')


def categories_view(request):
    categories = Category.objects.all().order_by('name')
    return render(request, 'categories.html', {'categories': categories})


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



class CartAddView(View):
    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=kwargs['pk'])
        try:
            quantity = int(request.POST.get('quantity', 1))
        except ValueError:
            quantity = 1
        if quantity < 1:
            quantity = 1

        cart_item = CartItem.objects.filter(product=product).first()
        in_cart = cart_item.quantity if cart_item else 0
        if in_cart + quantity <= product.stock:
            if cart_item:
                cart_item.quantity += quantity
                cart_item.save()
            else:
                CartItem.objects.create(product=product, quantity=quantity)

        next_url = request.POST.get('next')
        if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
            return redirect(next_url)
        return redirect('index')


def get_cart_context():
    cart_items = CartItem.objects.select_related('product').order_by('product__name')
    total = sum(item.get_total() for item in cart_items)
    return {'cart_items': cart_items, 'total': total}


class CartView(TemplateView):
    template_name = 'cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_cart_context())
        return context


class CartDeleteView(View):
    def post(self, request, *args, **kwargs):
        CartItem.objects.filter(product__pk=kwargs['pk']).delete()
        return redirect('cart')


class CartDecreaseView(View):
    def post(self, request, *args, **kwargs):
        cart_item = get_object_or_404(CartItem, product__pk=kwargs['pk'])
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
        return redirect('cart')