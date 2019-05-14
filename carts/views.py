from django.shortcuts import render
from .models import Cart


# Create your views here.


def cart_home(request):
	cart_obj = Cart.objects.new_or_get(request)
	# request.session['cart_id'] = "12"
	# cart_id = request.session.get("cart_id", None)
	# qs = Cart.objects.filter(id=cart_id)
	# if qs.count() == 1:
	# 	print('Cart Id exists')
	# 	cart_obj = qs.first()
	# 	if request.user.is_authenticated() and cart_obj.user is None:
	# 		cart_obj.user = request.user
	# 		cart_obj.save()
	# else:
	# 	cart_obj = Cart.objects.new(user=request.user)
	# 	request.session['cart_id'] = cart_obj.id
	# 	print("Cart Created")
	return render (request, "carts/home.html", {})
 