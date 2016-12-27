from django.contrib import admin
from catalog import models as mod
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'category_slug': ('category_name',)}
    list_display = ['category_name', 'pic', 'category_slug', 'category_isPublish', 'category_ordering']
    list_editable = ['category_slug', 'category_isPublish', 'category_ordering']
    search_fields = ['category_name']


class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ['name', 'pic']
    search_fields = ['name']


class ColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'pic']
    search_fields = ['name']


class ProductImagesInline(admin.StackedInline):
    model = mod.Images
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'product_slug':('product_name',)}
    list_display = ['product_category', 'product_name', 'pic', 'product_manufacturer', 'product_price',
                    'product_isPublish', 'product_ordering']
    list_editable = ['product_price','product_isPublish', 'product_ordering']
    inlines = [ProductImagesInline]
    list_filter = ['product_category', 'product_manufacturer']
    search_fields = ['product_name']


admin.site.register(mod.Category, CategoryAdmin)
admin.site.register(mod.Manufacturer, ManufacturerAdmin)
admin.site.register(mod.Color, ColorAdmin)
admin.site.register(mod.Product, ProductAdmin)
admin.site.register(mod.Material)
admin.site.register(mod.Size)
admin.site.register(mod.Density)
admin.site.register(mod.Attributes)
admin.site.register(mod.ProductModel)
admin.site.register(mod.ManCountry)
admin.site.register(mod.Promotions)