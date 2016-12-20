from django.db import models
from django.conf import settings
from mptt.models import MPTTModel, TreeForeignKey
from datetime import date, datetime
from Shop01.utils import ImageUploader

# Create your models here.

class Category(MPTTModel, ImageUploader):
    folder_name = 'category_name'
    category_name = models.CharField(max_length=255, blank=True, default='', verbose_name='Категория')
    parent = TreeForeignKey('self', null=True, blank=True, default=0, related_name='children')
    title = models.CharField(max_length=100, blank=True, default='', verbose_name='Заголовок категории')
    category_shortDescription = models.TextField(max_length=255, blank=True, default='', help_text='Краткое описание '
                                                                                                   'категории', verbose_name='Краткое описание')
    category_fullDescription = models.TextField(blank=True, verbose_name='Полное описание')
    category_image = models.ImageField(upload_to=ImageUploader.make_upload_path, default='', blank=True, verbose_name='Изображение' )
    category_slug = models.SlugField(max_length=255, blank=True, verbose_name='ЧПУ')
    metaDesc = models.CharField(max_length=200, blank=True, verbose_name='Мета-описание')
    metaKey = models.CharField(max_length=200,blank=True, verbose_name='Ключевые слова')
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

    def get_absolute_url(self):
        return "/cat/%id/" % self.id




class Material(models.Model):
    name = models.CharField(max_length=50, default='', verbose_name='Материал')
    material_description = models.CharField(max_length=200, blank=True, verbose_name='Описание')
    title = models.CharField(max_length=50, blank=True, verbose_name='Заголовок')
    metaDesc = models.CharField(max_length=100, blank=True, verbose_name='Мета описание')
    metaKey = models.CharField(max_length=150, default="", blank=True, verbose_name='Ключевые слова')

    def __str__(self):
        return self.name

    class Meta():
        verbose_name = 'Материал'
        verbose_name_plural = 'Материалы'


class Size(models.Model):
    name = models.CharField(max_length=40, default='', verbose_name='Размер')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'


class Color(models.Model, ImageUploader):
    folder_name = 'colors'
    name = models.CharField(max_length=40, verbose_name='Цвет')
    color_image = models.ImageField(upload_to=ImageUploader.make_upload_path, blank=True, verbose_name='Изображение' )

    def __str__(self):
        return self.name

    def pic(self):
        if self.color_image:
            return '<img src = "{}" width = "70" \>'.format(self.color_image.url)

    pic.allow_tag = True

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'


class ProductModel(models.Model):
    name = models.CharField(max_length=100, blank=True, verbose_name='Тип модели')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип модели'
        verbose_name_plural = 'Типы моделей'


class Manufacturer(models.Model, ImageUploader):
    folder_name = 'logo'
    name = models.CharField(max_length=50, blank=True, verbose_name='Производитель')
    manufacturer_logo = models.ImageField(upload_to=ImageUploader.make_upload_path, default='',blank=True, null=True, verbose_name='Логотип производителя')
    manufacturer_country = models.CharField(max_length=40, blank=True, verbose_name='Страна')

    def __str__(self):
        return self.name

    def pic(self):
        if self.manufacturer_logo:
            return '<img src="{}" width="70" \>'.format(self.manufacturer_logo.url)

    pic.short_description = 'Логотип'
    pic.allow_tag = True

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'


class Attributes(models.Model):
    name = models.CharField(max_length=30, blank=True, verbose_name='Дополнительные характеристики')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Дополнительный атрибут'
        verbose_name_plural = 'Дополнительные атрибуты'


class Density(models.Model):
    name = models.CharField(max_length=15, blank=True, verbose_name='Плотность')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Плотность'
        verbose_name_plural = 'Плотность'


class Product(models.Model, ImageUploader):
    folder_name = 'product_category'
    product_category = models.ForeignKey(Category, verbose_name='Категория', related_name='product_category')
    product_name = models.CharField(max_length=100, default='', verbose_name='Товар')
    product_manufacturer = models.ForeignKey(Manufacturer, blank=True, null=True, verbose_name='Производитель',
                                             related_name='product_manufacturer')
    product_model = models.ForeignKey(ProductModel, blank=True, null=True, verbose_name='Модель',
                                      related_name='product_model')
    product_density = models.ForeignKey(Density, blank=True, null=True, verbose_name='Плотность',
                                        related_name='product_density')
    product_material = models.ForeignKey(Material,blank=True, null=True, default=None, verbose_name='Материал',
                                         related_name='product_material')
    product_size = models.ManyToManyField(Size, verbose_name='Размер', related_name='product_size')
    product_color = models.ManyToManyField(Color, verbose_name='Цвет', related_name='product_color')
    product_attributes = models.ManyToManyField(Attributes, blank=True, null=True, verbose_name='Атрибуты',
                                                related_name='product_attributes')

    product_quantity = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Колличество на сайте')
    product_price = models.FloatField(null=True, verbose_name='Цена')
    product_image = models.ImageField(upload_to=ImageUploader.make_upload_path, blank=True, default='')
    product_description = models.TextField(verbose_name='Описание')
    title = models.CharField(max_length=50, blank=True, verbose_name='Заголовок')
    metaDesc = models.CharField(max_length=100, blank=True, verbose_name='Метаописание')
    metaKey = models.CharField(max_length=200, blank=True, verbose_name='Ключевые слова')
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


class Images(models.Model, ImageUploader):
    folder_name = 'images_productName'
    images_productName = models.ForeignKey(Product, blank=True, null=True, verbose_name='Продукт')
    images_productImage = models.ImageField(upload_to=ImageUploader.make_upload_path, verbose_name='Изображение')

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


