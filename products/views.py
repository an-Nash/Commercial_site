from django.views.generic import ListView, DetailView
from django.http import Http404
from django.shortcuts import render

from .models import Product
from carts.models import Cart
from analytics.mixins import ObjectViewedMixin

# Create your views here.


class ProductFeaturedListView(ListView):
	# queryset = Product.objects.all()
	template_name = "products/list.html"

	def get_queryset(self, *args, **kwargs):
		request = self.request
		return Product.objects.all().featured()


class ProductFeaturedDetailView(ObjectViewedMixin, DetailView):
	# queryset = Product.objects.all()
	template_name = "products/featured-detail.html"

	
	def get_queryset(self, *args, **kwargs):
		request = self.request
		return Product.objects.all().featured()


class ProductDetailSlugView(ObjectViewedMixin, DetailView):
	queryset = Product.objects.all()
	template_name = "products/detail.html"


	def get_context_data(self, *args, **kwargs):
		context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
		cart_obj, new_obj = Cart.objects.new_or_get(self.request)
		context['cart'] = cart_obj
		return context


	def get_object(self, *args, **kwargs):
		request = self.request
		slug = self.kwargs.get('slug')
		# instance = Product.objects.get_by_id(pk)
		try:
			instance = Product.objects.get(slug=slug)
		except Product.DoesNotExist:
			raise Http404("Not found..")
		except Product.MultipleObjectsReturned:
			qs = Product.objects.filter(slug=slug)
			instance = qs.first()
		except:
			raise Http404("Uhhmmm")
		return instance





class ProductListView(ListView):
	queryset = Product.objects.all()
	template_name = "products/list.html"

	# def get_context_data(self,*args,**kwargs): #for seeing what object are passing through the context(not necessary)
	# 	context = super(ProductListView,self).get_context_data(*args, **kwargs)
	# 	print(context)
	# 	return context

	def get_queryset(self, *args, **kwargs):
		request = self.request
		return Product.objects.all()




class ProductDetailView(ObjectViewedMixin, DetailView):
	queryset = Product.objects.all()
	template_name = "products/detail.html"

	# def get_context_data(self,*args,**kwargs): #for seeing what object are passing through the context(not necessary)
	# 	context = super(ProductListView,self).get_context_data(*args, **kwargs)
	# 	print(context)
	# 	return context

	def get_object(self, *args, **kwargs):
		request = self.request
		pk = self.kwargs.get('pk')
		instance = Product.objects.get_by_id(pk)
		if instance is None:
			raise Http404("Product doesn't exist")
		return instance



def product_detail_view(request,pk, *args, **kwargs):
	# qs = Product.objects.filter(id=pk)
	# if qs.exists() and qs.count()==1:
	# 	instance = qs.first()
	# else:
	# 	raise Http404("Product doesn't exists")

	instance = Product.objects.get_by_id(pk)
	if instance is None:
		raise Http404("Product doesn't exists")

	context={
	'object': instance
	}
	return render(request, "products/detail.html", context)