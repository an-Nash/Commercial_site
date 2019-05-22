from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)



class RegisterForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(
		attrs={"class":"form-control",}))
	email    = forms.EmailField(widget=forms.EmailInput(
		attrs={"class":"form-control",}))
	password = forms.CharField(widget=forms.PasswordInput)
	password2 = forms.CharField(label='Confirm password',widget=forms.PasswordInput)

	def clean(self):
		data = self.cleaned_data
		password = self.cleaned_data.get('password')
		password2 = self.cleaned_data.get('password2')
		if password != password2:
			raise forms.ValidationError("password must match")
		return data

	def clean_username(self):
		username = self.cleaned_data.get('username')
		qs = User.objects.filter(username=username)
		if qs.exists():
			raise forms.ValidationError("username is taken")
		return username