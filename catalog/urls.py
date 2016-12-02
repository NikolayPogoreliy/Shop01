from django.conf.urls import url
from catalog.views import CategorysListView, ProductDetailView
from django.shortcuts import render

urlpatterns = [
    url(r'^cat/(?:(?P<cat_id>\d*)/)$', CategorysListView.as_view(), name='categories'),
    url(r'^prod/(?:(?P<prod_id>\d*)/)$', ProductDetailView.as_view(), name='product'),
    url(r'^$', 'catalog.views.simple_test', name='home'),
]