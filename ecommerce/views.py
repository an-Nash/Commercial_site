from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from .forms import ContactForm

def home_page(request):
	context = {
	"title":"welcome to the home page"
	}
	if request.user.is_authenticated:
		context["premium_content"] = "yeahhh"
	return render(request, "home_page.html", context)

def about_page(request):
	context = {
	"title":"welcome to the about page"
	}
	return render(request, "about.html", context)

def contact_page(request):
	contact_form = ContactForm(request.POST or None)
	context = {
	"title":"welcome to the Contact page",
	"form" : contact_form
	}
	if contact_form.is_valid():
		print(contact_form.cleaned_data)
		if request.is_ajax():
			return JsonResponse({"message": "Thank you for your submission"})


	if contact_form.errors:
		error = contact_form.errors.as_json()
		if request.is_ajax():
			return HttpResponse(error, status=400, content_type='application/json')
	print(request.POST)
	return render(request, "contact/view.html", context)
