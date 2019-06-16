from django.db import models
from django.conf import settings

from products.models import Product
import os
from django.db.models.signals import pre_save,post_save, m2m_changed


User = settings.AUTH_USER_MODEL
# Create your models here.

class CartManager(models.Manager):
	def new_or_get(self, request):
		cart_id = request.session.get("cart_id", None)         #Cart id session creating
		qs = Cart.objects.filter(id=cart_id)                   #Lookup cart session as id
		if qs.count() == 1:
			new_obj = False
			print('Cart Id exists')                            #If session exists then cart is also exists
			cart_obj = qs.first()                              #Reassign existing session as first 
			if request.user.is_authenticated() and cart_obj.user is None:  #if user authenticated and user of cart is null-->then
				cart_obj.user = request.user                   #Assign user who is requesting as current user of current cart obj
				cart_obj.save()                                #Save user and current null cart for the user
		else:                                                  #cart doesnt exist neither user
			cart_obj = Cart.objects.new(user=request.user)     #creating user of the current cart
			new_obj = True
			request.session['cart_id'] = cart_obj.id           #creating new session for new cart
			print("Cart Created")
		return cart_obj, new_obj


	def new(self, user=None):                                  #new method for creating new user
		user_obj = None
		if user is not None:
			if user.is_authenticated():
				user_obj = user
		return self.model.objects.create(user=user_obj)


class Cart(models.Model):
	user     	= models.ForeignKey(User, null=True, blank= True)
	products 	= models.ManyToManyField(Product, blank=True)
	total		= models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
	subtotal	= models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
	updated		= models.DateTimeField(auto_now=True)
	timestamp	= models.DateTimeField(auto_now_add=True)

	objects = CartManager()

	def __str__(self):
		return str(self.id)


def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
	if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
		products = instance.products.all()
		total = 0
		for x in products:
			total+=x.price
		instance.subtotal = total
		instance.save()

m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.products.through)


def pre_save_cart_receiver(sender, instance, *args, **kwargs):
	if instance.subtotal > 0:
		instance.total = instance.subtotal +10
	else:
		instance.subtotal = 0

pre_save.connect(pre_save_cart_receiver, sender=Cart)