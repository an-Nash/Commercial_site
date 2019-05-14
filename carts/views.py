from django.shortcuts import render
from .models import Cart


# Create your views here.
def cart_create(user=None):
	cart_obj = Cart.objects.create(user=None)
	print("New Cart created")
	return cart_obj



def cart_home(request):
	request.session['cart_id'] = "12"
	cart_id = request.session.get("cart_id", None)
	# if cart_id is None:
	# 	cart_obj = cart_create()
	# 	request.session['cart_id'] = ca.id
	# # del request.session['cart_id']
	qs = Cart.objects.filter(id=cart_id)
	if qs.count() == 1:
		print('Cart Id exicts')
		cart_obj = qs.first()
	else:
		cart_obj = cart_create()
		request.session['cart_id'] = cart_obj.id
	return render (request, "carts/home.html", {})
 