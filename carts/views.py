from django.shortcuts import render, redirect
from django.core.exceptions import MultipleObjectsReturned

from .models import Cart
from orders.models import Order
from accounts.forms import LoginForm, GuestForm
from billing.models import BillingProfile
from accounts.views import guest_register_view

from products.models import Product
from accounts.models import GuestEmail


# Create your views here.


def cart_home(request):
	cart_obj, new_obj = Cart.objects.new_or_get(request)
	return render (request, "carts/home.html", {"cart":cart_obj})
 

def cart_update(request):
	product_id = request.POST.get('product_id')#getting id of the product
	if product_id is not None:
		try:
			product_obj = Product.objects.get(id=product_id)
		except Product.DoesNotExist:
			print("Product is gone?")
			return redirect("cart:home")
		cart_obj, new_obj = Cart.objects.new_or_get(request)
		if product_obj in cart_obj.products.all():
			cart_obj.products.remove(product_obj)
		else:
			cart_obj.products.add(product_obj)
		request.session['cart_item'] = cart_obj.products.count()

	return redirect("cart:home")

 	# return redirect(product_obj.get_absolute_url())

def checkout_home(request):

	# try:
 #    	Cart.objects.get(cart=cart)
	# except MultipleObjectsReturned:
 #    	Cart.objects.filter(cart=cart).first()

 	cart_obj, cart_created = Cart.objects.new_or_get(request)
 	order_obj = None

 	if cart_created or cart_obj.products.count() == 0:
 		return redirect("cart:home")
 	else:
 		order_obj, new_order_obj = Order.objects.get_or_create(cart=cart_obj)


 	user = request.user
 	billing_profile = None
 	login_form = LoginForm()
 	guest_form = GuestForm()
 	guest_email_id = request.session.get('guest_email_id')

 	if user.is_authenticated():
 		billing_profile, billing_created = BillingProfile.objects.get_or_create(user=user, email=user.email)

 	elif guest_email_id is not None:
 		guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
 		billing_profile, billing_guest_created = BillingProfile.objects.get_or_create(email=guest_email_obj.email)
 	else:
 		pass

 	# if billing_profile is not None:
 	# 	order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
 	

 	context = {
 	"object":order_obj,
 	"billing_profile": billing_profile,
 	"guest_form" : guest_form,
 	"login_form" : login_form
 	}
 	return render(request, "carts/checkout.html", context)