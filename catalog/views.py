from django.shortcuts import render, render_to_response, get_object_or_404
from catalog.models import *
from django.views.generic.list import ListView
from mptt.querysets import *
from django.views.generic.detail import DetailView
# Create your views here.


#TODO: test only. must be teleted
def simple_test(request):
    return render(request, 'index.html')


def get_product_attr(objects, keys):
    attr = { key: set() for key in keys}
    for object in objects:
        attr['product_color'].update(object.product_color.filter(product_color=object.id))
        attr['product_sizes'].update(object.product_size.filter(product_size=object.id))
        attr['product_material'].add(object.product_material)
        attr['product_manufacturer'].add(object.product_manufacturer)
        attr['product_model'].add(object.product_model)
        attr['product_attributes'].update(object.product_attributes.filter(product_attributes=object.id))
    return attr



class CategorysListView(ListView):
    template_name = 'base.html'
    queryset = Category.objects.all()

    def get(self, request, *arg, **kwargs):
        if self.kwargs['cat_id']: 
            self.cat_id = self.kwargs['cat_id']

        return super(CategorysListView, self).get(request, *arg, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CategorysListView,self).get_context_data(**kwargs)
        cat = get_object_or_404(Category, id=self.cat_id)      #Вытягиваем указанную категорию
                                                                #Если категории с таким ID нет - page404

        context['category'] = cat
        context['subcat'] = cat.get_children() #Дочерние (на уровень ниже) категории для отображения в подменю
        context['ancestor'] = cat.get_ancestors(ascending=False, include_self=True) #Все родительские категории для
                                                                                    # хлебных крошек
        descendants = cat.get_descendants(include_self=True)    # Получаем всех потомков (от текущего уровня и до листа,
                                                                #  по всем ветвям), родителем которых является заданная
                                                                # категория
        # Получаем общий список товаров для всех категорий-потомков, и текущей категории
        #context['products'] = []
        products = []
        for category in descendants:
            #context['products'].extend(Product.objects.filter(product_category_id=category.id))
            products.extend(Product.objects.filter(product_category_id=category.id))

        context['products'] = products
        # Формируем наборы (множества) дополнительных атрибутов товаров для фильтрации
        # context['color'] = set()
        # context['sizes'] = set()
        # context['material'] = set()
        # context['manuf'], context['model'], context['attrs'] = set(), set(), set()
        keys = [
            'product_color',
            'product_sizes',
            'product_material',
            'product_model',
            'product_manufacturer',
            'product_attributes',
        ]

        context.update(get_product_attr(products, keys))
        # for prod in context['products']:
        #     context['color'].update(prod.product_color.filter(product_color=prod.id))
        #     context['sizes'].update(getattr(prod,'product_size').filter(product_size=prod.id))
        #     try:
        #         context['material'].update(getattr(prod,'product_material').filter(product_material=prod.product_material))
        #     except:
        #         context['material'].add(getattr(prod,'product_material'))
        #     context['manuf'].add(prod.product_manufacturer)
        #     context['model'].add(prod.product_model)
        #     context['attrs'].update(prod.product_attributes.filter(product_attributes=prod.id))
        return context


class ProductDetailView(DetailView):
    template_name = 'product.html'
    queryset = Product.objects.all()
    pk_url_kwarg = 'prod_id'
    context_object_name = 'prod'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)

        prod = context['prod']
        context['color'] = prod.product_color.filter(product_color=prod.id) #TODO: may be to DELETE
        context['crombs'] = Category.objects.get(id=prod.product_category_id).get_ancestors(include_self=True)

        return context


