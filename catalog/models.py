from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from datetime import date

# Create your models here.
# TODO: define function for image upload path generation


class Category(MPTTModel):
    category_name = models.CharField(max_length=255, blank=True, default='', verbose_name='Категория')
    category_parrent = TreeForeignKey('self', null=True, blank=True, default=0, related_name='children')
    category_title = models.CharField(max_length=100, blank=True, default='', verbose_name='Заголовок категории')
    category_shortDescription = models.TextField(max_length=255, blank=True, default='', help_text='Краткое описание '
                                                                                                   'категории', verbose_name='Краткое описание')
    category_fullDescription = models.TextField(blank=True, verbose_name='Полное описание')
    category_image = models.ImageField(upload_to='',default='', blank=True, verbose_name='Изображение' )  # TODO: set image upload path with category name as folder name
    # todo: set default image path

    category_slug = models.SlugField(max_length=255, blank=True, verbose_name='ЧПУ')
    category_metaDesc = models.CharField(max_length=200, blank=True, verbose_name='Мета-описание')
    category_metaKey = models.CharField(max_length=200,blank=True, verbose_name='Ключевые слова')
    category_isPublish = models.BooleanField(default=False, verbose_name='Опубликовать')
    category_ordering = models.IntegerField(default=0, blank=True, null=True, verbose_name='Порядок сортировки')

    def __str__(self):
        return self.category_name

    def pic(self):
        if self.category_image:
            return '<img src = "%s" width="70" \>' % self.category_image.url

    pic.short_description = 'Изображение'
    pic.allow_tag = True

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    class MPTTMeta:
        order_insertion_by = ['category_name']


class Material(models.Model):
    material_name = models.CharField(max_length=50, default='', verbose_name='Материал')
    material_description = models.CharField(max_length=200, blank=True, verbose_name='Описание')
    material_title = models.CharField(max_length=50, blank=True, verbose_name='Заголовок')
    material_metaDesc = models.CharField(max_length=100, blank=True, verbose_name='Мета описание')
    material_metaKey = models.CharField(max_length=150, default="", blank=True, verbose_name='Ключевые слова')

    def __str__(self):
        return self.material_name

    class Meta():
        verbose_name = 'Материал'
        verbose_name_plural = 'Материалы'


class Size(models.Model):
    size_name = models.CharField(max_length=40, default='', verbose_name='Размер')

    def __str__(self):
        return self.size_name

    class Meta:
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'


class Color(models.Model):
    color_name = models.CharField(max_length=40, verbose_name='Цвет')
    color_image = models.ImageField(upload_to='', blank=True, verbose_name='Изображение' )  # TODO: set image upload path with category name as folder name

    def __str__(self):
        return self.color_name

    def pic(self):
        if self.color_image:
            return '<img src = "{}" width = "70" \>'.format(self.color_image.url)

    pic.allow_tag = True

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'


class ProductModel(models.Model):
    productModel_name = models.CharField(max_length=100, blank=True, verbose_name='Тип модели')

    def __str__(self):
        return self.productModel_name

    class Meta:
        verbose_name = 'Тип модели'
        verbose_name_plural = 'Типы моделей'


class Manufacturer(models.Model):
    manufacturer_name = models.CharField(max_length=50, blank=True, verbose_name='Производитель')
    manufacturer_logo = models.ImageField(upload_to='', default='', verbose_name='Логотип производителя')
    manufacturer_country = models.CharField(max_length=40, blank=True, verbose_name='Страна')

    def __str__(self):
        return self.manufacturer_name

    def pic(self):
        if self.manufacturer_logo:
            return '<img src="{}" width="70" \>'.format(self.manufacturer_logo.url)

    pic.short_description = 'Логотип'
    pic.allow_tag = True

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'


class Product(models.Model):
    product_category = models.ForeignKey(Category, verbose_name='Категория', related_name='product_category')
    product_name = models.CharField(max_length=100, default='', verbose_name='Товар')
    product_manufacturer = models.ForeignKey(Manufacturer, blank=True, null=True, verbose_name='Производитель')
    product_model = models.ForeignKey(ProductModel, blank=True, null=True, verbose_name='Модель')
    product_size = models.ManyToManyField(Size, verbose_name='Размер', related_name='product_size')
    product_color = models.ManyToManyField(Color, verbose_name='Цвет', related_name='product_color')
    product_quantity = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Колличество на сайте')
    product_price = models.PositiveSmallIntegerField(null=True, verbose_name='Цена')
    product_image = models.ImageField(upload_to='', blank=True, default='')#TODO: set image upload function
    product_description = models.TextField(verbose_name='Описание')
    product_title = models.CharField(max_length=50, blank=True, verbose_name='Заголовок')
    product_metaDescription = models.CharField(max_length=100, blank=True, verbose_name='Метаописание')
    product_metaKey = models.CharField(max_length=200, blank=True, verbose_name='Ключевые слова')
    product_slug = models.SlugField(max_length=20, blank=True, verbose_name='ЧПУ')
    product_views = models.PositiveSmallIntegerField(null=True, editable=False, verbose_name='Колличество просмотров')
    product_comments = models.PositiveSmallIntegerField(null=True, editable=False, verbose_name='Колличество комментариев')
    product_isPublish = models.BooleanField(default=0, verbose_name='Опубликовать')
    product_ordering = models.PositiveSmallIntegerField(null=True, default=255, verbose_name='Порядок сортировки')
    product_pubDate = models.DateField(default=date.today(), verbose_name='Дата публикации на сайте', help_text='Для отложенной публикации установите будущую дату')

    def __str__(self):
        return self.product_name

    def pic(self):
        if self.product_image:
            return '<img src="{}" width="70" \>'.format(self.product_image.url)

    pic.short_description = 'Изображение'
    pic.allow_tags = True

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Images(models.Model):
    images_productName = models.ForeignKey(Product, blank=True, null=True, verbose_name='Продукт')
    images_productImage = models.ImageField(upload_to='', verbose_name='Изображение') #TODO: set image upload function

    def __str__(self):
        return self.images_productImage.url

    def pic(self):
        if self.images_productImage:
            return '<img src="%s" width="70"/>' % self.images_productImage.url
        else:
            return '(none)'

    pic.short_description = 'Изображение'
    pic.allow_tags = True

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
