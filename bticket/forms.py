from django import forms
import re
from django.contrib.auth.models import User
from django.forms import ModelForm
from bticket.models import *
from bticket.utils.widgets import AdminImageWidget
from django.contrib.auth.forms import PasswordResetForm

from django.utils.safestring import mark_safe


class OnTheFlyTicketForm(ModelForm):
	class Meta:
		model = OnTheFlyTicket
		exclude = ('recovery_code', 'emission_date', 'qr_code')
	email = forms.EmailField(label = u'Email')

class RecoveryOnTheFlyTicketForm(forms.Form):
	recovery_code = forms.CharField(label = u'Recovery Code', max_length = 100)

class SentEmailFromRecoveryForm(forms.Form):
	email = forms.EmailField(label = u'Email')

class CheckNuberOfTripsForm(forms.Form):
	code = forms.CharField(label = u'Recovery Code', max_length = 100)

class UserProfileRegistrationForm(ModelForm):
	first_name_error = {
		'required': mark_safe('<div class="alert alert-error" style="max-width:145px">First name is required.</div>')
	}

	first_name = forms.CharField(label = u'First Name', max_length = 30, error_messages = first_name_error)
	
	last_name_error = {
		'required': mark_safe('<div class="alert alert-error" style="max-width:145px">Last name is required.</div>')
	}
	last_name = forms.CharField(label = u'Last Name', max_length = 30, error_messages = last_name_error)
	
	email_errors = {
		'required': mark_safe('<div class="alert alert-error" style="max-width:145px">Email is required.</div>'),
		'invalid': mark_safe('<div class="alert alert-error" style="max-width:300px">Invalid email.<br>It must follow the pattern: name@domain.com.</div>')
	}
	email = forms.EmailField(label = u'Email', error_messages = email_errors)

	username_error = {
		'required': mark_safe('<div class="alert alert-error" style="max-width:145px">Username is required.</div>')
	}
	username = forms.CharField(label = u'Username', max_length = 30, error_messages = username_error)
	
	pass1_error = {
		'required': mark_safe('<div class="alert alert-error" style="max-width:145px">Password is required.</div>')
	}
	password1 = forms.CharField(
		label = u'Password',
		widget = forms.PasswordInput(),
		error_messages = pass1_error
	)
	pass2_error = {
		'required': mark_safe('<div class="alert alert-error" style="max-width:175px">Re-type password is required.</div>')
	}
	password2 = forms.CharField(
		label = u'Password(Again)',
		widget = forms.PasswordInput(),
		error_messages = pass2_error
	)

	class Meta:
		model = UserProfile
		exclude = ('username')
		field_args = {
			"avatar" : {
				"error_messages" : {
					'required': mark_safe('<div class="alert alert-error" style="max-width:145px">Avataard is required.</div>')
				}
			}
		}
		
	def clean_password2(self):
		if 'password1' in self.cleaned_data:
			password1 = self.cleaned_data['password1']
			password2 = self.cleaned_data['password2']
			if password1 == password2:
				return password2
		raise forms.ValidationError(mark_safe('<div class="alert alert-error" style="max-width:145px">Passwords do not match.</div>'))
		
	def clean_username(self):
		username = self.cleaned_data['username']
		if not re.search(r'^\w+$', username):
			raise forms.ValidationError(mark_safe('<div class="alert alert-error" style="max-width:145px">Username can only contain '
				'alphanumeric characters and the underscore.</div>'))
		try:
			User.objects.get(username = username)
		except:
			return username
		raise forms.ValidationError(mark_safe('<div class="alert alert-error" style="max-width:145px">Username is already taken.</div>'))

	def clean_first_name(self):
		first_name = self.cleaned_data['first_name']
		if not re.search(r'(?iL)^[\s\*\?a-z]*$', first_name):
			raise forms.ValidationError(mark_safe('<div class="alert alert-error" style="max-width:145px">First name can only contain '
				'a-z letters and whitespaces.</div>'))
		try:
			User.objects.get(first_name = first_name)
		except:
			return first_name

	def clean_last_name(self):
		last_name = self.cleaned_data['last_name']
		if not re.search(r'(?iL)^[\s\*\?a-z]*$', last_name):
			raise forms.ValidationError(mark_safe('<div class="alert alert-error" style="max-width:145px">Last name can only contain '
				'a-z letters and whitespaces.</div>'))
		try:
			User.objects.get(last_name = last_name)
		except:
			return last_name

class UserProfileManagementForm(ModelForm):
	class Meta:
		model = UserProfile
		exclude = ('username')
	
	first_name = forms.CharField(label = u'First Name', max_length = 30)
	last_name = forms.CharField(label = u'Last Name', max_length = 30)	
	email = forms.EmailField(label = u'Email')
	avatar = forms.FileField(widget = AdminImageWidget, required = False)
	
	
	

class BuyTicketForm(ModelForm):
	class Meta:
		model = Ticket
		exclude = ('user', 'qr_code', 'emission_date')

class BuyPassForm(ModelForm):
	class Meta:
		model = Pass
		exclude = ('username', 'qr_code', 'emission_date', 'expiration_date')

