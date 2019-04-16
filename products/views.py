from django.views.generic import ListView, DetailView
from django.shortcuts import render

from .models import Product

# Create your views here.

class ProductListView(ListView):
	queryset = Product.objects.all()
	template_name = "products/list.html"

	# def get_context_data(self,*args,**kwargs): #for seeing what object are passing through the context(not necessary)
	# 	context = super(ProductListView,self).get_context_data(*args, **kwargs)
	# 	print(context)
	# 	return context

class ProductDetailView(DetailView):
	queryset = Product.objects.all()
	template_name = "products/detail.html"

	# def get_context_data(self,*args,**kwargs): #for seeing what object are passing through the context(not necessary)
	# 	context = super(ProductListView,self).get_context_data(*args, **kwargs)
	# 	print(context)
	# 	return context