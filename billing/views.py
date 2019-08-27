from django.shortcuts import render

# Create your views here.
import stripe
stripe.api_key = "sk_test_ZcsfoeeilUpgqPWvntcnP5gH00P3pdKvTc"
STRIPE_PUB_KEY = 'pk_test_htvvpbeMLHMt1ztiZsJXQ78z00Z2ykHcXr'


def payment_method_view(request):
	if request.method == "POST":
		print(request.POST)
	return render(request, 'billing/payment-method.html', {"publish_key": STRIPE_PUB_KEY})