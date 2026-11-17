from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False, blank=False, verbose_name="Наименование")
    description = models.TextField(max_length=1000, null=True, blank=True, verbose_name="Описание")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name="Наименование")
    description = models.TextField(max_length=1000, null=True, blank=True, verbose_name="Описание")
    category = models.ForeignKey('webapp.Category', related_name='products', null=False, on_delete=models.CASCADE, verbose_name="Категория")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    price = models.DecimalField(max_digits=7, decimal_places=2, null=False, blank=False, verbose_name="Стоимость")
    image = models.URLField(max_length=1000, null=False, blank=False, verbose_name="Изображение")
    stock = models.PositiveIntegerField(default=0, verbose_name='Остаток')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class CartItem(models.Model):
    product = models.ForeignKey('webapp.Product', related_name='cart_items', on_delete=models.CASCADE,
                                verbose_name='Товар')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    def get_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f'{self.product.name} x {self.quantity}'

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'


class Order(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    phone = models.CharField(max_length=30, verbose_name='Телефон')
    address = models.CharField(max_length=200, verbose_name='Адрес')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    products = models.ManyToManyField('webapp.Product', through='webapp.OrderProduct',
                                      related_name='orders', verbose_name='Товары')

    def __str__(self):
        return f'Заказ #{self.pk} — {self.name}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderProduct(models.Model):
    order = models.ForeignKey('webapp.Order', related_name='order_products', on_delete=models.CASCADE,
                              verbose_name='Заказ')
    product = models.ForeignKey('webapp.Product', related_name='order_products', on_delete=models.CASCADE,
                                verbose_name='Товар')
    quantity = models.PositiveIntegerField(verbose_name='Количество')

    def __str__(self):
        return f'{self.product.name} x {self.quantity}'

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'