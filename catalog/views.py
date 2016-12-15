from django.shortcuts import render, get_object_or_404
from catalog.models import *
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib import sessions
from django.conf import settings
# Create your views here.


#TODO: test only. must be teleted
def simple_test(request):
    return render(request, 'index.html')

sort = 0
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
    template_name = settings.VIEW_SET[0]
    paginate_by = settings.LIMITS_SET[0]
    sort = 0

    products = []
    cat = None
    keys = [
        'product_color',
        'product_size',
        'product_attributes',
        'product_material',
        'product_model',
        'product_manufacturer',
    ]

    def get(self, request, *arg, **kwargs):
        if self.kwargs['cat_id']: 
            cat_id = self.kwargs['cat_id']
            self.cat = get_object_or_404(Category, id=cat_id)
        #if request.GET:
        try:
            self.sort = request.GET['sort']
            request.session['sort'] = self.sort
        except:
            self.sort = request.session.get('sort',0)

        try:
            self.paginate_by = int(request.GET['limits'])
            request.session['limits'] = self.paginate_by
        except:
            self.paginate_by = int(request.session.get('limits', settings.LIMITS_SET[0]))

        try:
            template = int(request.GET['view'])
            request.session['view'] = template
        except:
            template = int(request.session.get('view', 0))
        self.template_name = settings.VIEW_SET[template]
        return super(CategorysListView, self).get(request, *arg, **kwargs)


    def get_context_data(self, **kwargs):
        context = super(CategorysListView,self).get_context_data(**kwargs)
        context['category'] = self.cat
        context['subcat'] = self.cat.get_children() #Дочерние (на уровень ниже) категории для отображения в подменю
        context['crumbs'] = self.cat.get_ancestors(ascending=False, include_self=True) #Все родительские категории для

        context['sort_options'] = [option[1] for option in settings.PRODUCT_ORDERING_SET]
        context['limit_option'] = settings.LIMITS_SET
        context.update(get_product_attr(self.keys, *self.products))
        return context

    def get_queryset(self):
        # Получаем общий список товаров для всех категорий-потомков, и текущей категории
        #self.products = Product.objects.filter(product_category__in=self.cat.get_descendants(include_self=True)
         #                                      ).order_by(settings.PRODUCT_ORDERING_SET[int(self.sort)][0])
        return Product.objects.filter(product_category__in=self.cat.get_descendants(include_self=True)
                                      ).order_by(settings.PRODUCT_ORDERING_SET[int(self.sort)][0])


class ProductDetailView(DetailView):
    template_name = 'product.html'
    queryset = Product.objects.all()
    pk_url_kwarg = 'prod_id'
    context_object_name = 'product'
    keys = [
        'product_color',
        'product_size',
        'product_attributes',
    ]

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)

        product = context['product']
        context['crumbs'] = Category.objects.get(id=product.product_category_id).get_ancestors(include_self=True)

        context.update(get_product_attr(self.keys, product))
        return context


