from django.http import HttpResponse
from django.shortcuts import render

from .forms import ContactForm

def home_page(request):
	context = {
	"title":"welcome to the home page"
	}
	return render(request, "home_page.html", context)

def about_page(request):
	context = {
	"title":"welcome to the about page"
	}
	return render(request, "home_page.html", context)

def contact_page(request):
	contact_form = ContactForm(request.POST or None)
	context = {
	"title":"welcome to the about page",
	"form" : contact_form
	}
	if contact_form.is_valid():
		print(contact_form.cleaned_data)
	print(request.POST)
	return render(request, "contact/view.html", context)
