from django.shortcuts import render, get_object_or_404
from catalog.models import *
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.conf import settings
# Create your views here.


#TODO: test only. must be teleted
def simple_test(request):
    return render(request, 'index.html')


def get_product_attr(keys, *args):
    ''' Return dict with atttributes of one object, or sets of attributes for many objects
    keys - list of attributes name (i.e. names of needed fields of record(s))
    args - object, or list of objects
            (a = get_product_attr(keys, obj) for one object)
            (a = get_product_attr(keys, *obj) for many objects)
    return -> {key:{attr, ...}, ...}
    '''
    attr = {key: set() for key in keys}
    for object in args:
        for key in keys:
            try:
                attr[key].update(getattr(object,key).all())
            except:
                attr[key].add(getattr(object, key))

    return attr



class CategorysListView(ListView):
    template_name = 'base.html'
    queryset = Category.objects.all()
    sort = 0
    selected = ''
    def get(self, request, *arg, **kwargs):
        if self.kwargs['cat_id']: 
            self.cat_id = self.kwargs['cat_id']
        if request.GET:
            self.sort = request.GET.get('sort', 0)
            self.selected = 'sel_'+str(self.sort)
        return super(CategorysListView, self).get(request, *arg, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CategorysListView,self).get_context_data(**kwargs)
        cat = get_object_or_404(Category, id=self.cat_id)   #Вытягиваем указанную категорию
                                                            #Если категории с таким ID нет - page404

        context['category'] = cat
        context['subcat'] = cat.get_children() #Дочерние (на уровень ниже) категории для отображения в подменю
        context['crumbs'] = cat.get_ancestors(ascending=False, include_self=True) #Все родительские категории для
                                                                                    # хлебных крошек
        descendants = cat.get_descendants(include_self=True)    # Получаем всех потомков (от текущего уровня и до L2,
                                                                #  по всем ветвям), родителем которых является заданная
                                                                # категория
        # Получаем общий список товаров для всех категорий-потомков, и текущей категории
        #products = []
        #for category in descendants:
            #products.extend(Product.objects.filter(product_category=category))
        sort_method = settings.PRODUCT_ORDERING_SET[int(self.sort)][0]
        products = Product.objects.filter(product_category__in=descendants).order_by(sort_method)
        context['products'] = products
        keys = [
            'product_color',
            'product_size',
            'product_attributes',
            'product_material',
            'product_model',
            'product_manufacturer',
            ]
        context['sort_options'] = [option[1] for option in settings.PRODUCT_ORDERING_SET]
        #context['sort'] = settings.PRODUCT_ORDERING_SET[int(self.sort)][0]
        #context['sort'] = self.sort
        context['selected'] = self.selected

        context.update(get_product_attr(keys, *products))
        return context


class ProductDetailView(DetailView):
    template_name = 'product.html'
    queryset = Product.objects.all()
    pk_url_kwarg = 'prod_id'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)

        product = context['product']
        #context['color'] = product.product_color.filter(product_color=product.id) #TODO: may be to DELETE
        context['crumbs'] = Category.objects.get(id=product.product_category_id).get_ancestors(include_self=True)
        keys=[
            'product_color',
            'product_size',
            'product_attributes',
        ]
        context.update(get_product_attr(keys, product))
        return context


