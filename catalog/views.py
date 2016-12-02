from django.shortcuts import render, render_to_response, get_object_or_404
from catalog.models import *
from django.views.generic.list import ListView
from mptt.querysets import *
from django.views.generic.detail import DetailView
# Create your views here.


#TODO: test only. must be teleted
def simple_test(request):
    return render(request, 'index.html')

class CategorysListView(ListView):
    template_name = 'base.html'
    queryset = Category.objects.all()

    def get(self, request, *arg, **kwargs):
        if self.kwargs['cat_id']: 
            self.cat_id = self.kwargs['cat_id']

        return super(CategorysListView, self).get(request, *arg, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CategorysListView,self).get_context_data(**kwargs)
        cat = get_object_or_404(Category, id=self.cat_id)
        descendants = cat.get_descendants(include_self=True)
        context['category'] = cat
        context['subcat'] = Category.objects.filter(parent_id=self.cat_id).order_by('category_ordering')
        context['products'] = []
        context['ancestor'] = cat.get_ancestors(ascending=False, include_self=True)

        for category in descendants:
            context['products'].extend(Product.objects.filter(product_category_id=category.id))

        return context


class ProductDetailView(DetailView):
    template_name = 'product.html'
    queryset = Product.objects.all()
    pk_url_kwarg = 'prod_id'
    context_object_name = 'prod'

    # def get(self, request, *arg, **kwargs):
    #     if kwargs['prod_id']:
    #         self.prod_id = kwargs['prod_id']
    #
    #     return super(ProductDetailView, self).get(self, request, *arg, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        #prod = get_object_or_404(Product, id=self.prod_id)
        prod = context['prod']
        context['crombs'] = Category.objects.get(id=prod.product_category_id).get_ancestors(include_self=True)

        return context


