from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import Context, RequestContext
from django.template.loader import get_template
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from bticket.forms import *
from uid import generator as g
from bticket.models import *
import hashlib, sys, qrcode
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from settings import *
from os import remove

# Create your views here.
def main_page(request):
	if request.method == 'POST':
		form = OnTheFlyTicketForm(request.POST)
		if form.is_valid():
			generated_str = g.id_generator(10)
			while OnTheFlyTicket.objects.filter(recovery_code = generated_str):
				generated_str = g.id_generator(10)
			
			generated_qrc_str = g.id_generator(8)
			generated_qrc = hashlib.sha1('bticketcode').hexdigest() + generated_qrc_str
			while OnTheFlyTicket.objects.filter(qr_code = generated_qrc):
				generated_qrc_str = g.id_generator(8)
				generated_qrc = hashlib.sha1('bticketcode').hexdigest() + generated_qrc_str
			
			qrcode_obj = QRCode.objects.create(qr_code = generated_qrc)
			
			ticket = form.save(commit = False)
			ticket.recovery_code = generated_str
			ticket.qr_code =  qrcode_obj
			ticket.save()
			
			mail_subject = 'bTicket|OntheFly Purchase'
			mail_body = 'Ticket information: \n\n \tRecovery Code:\n\t' +  ticket.recovery_code + "\n \tQR Code:\n\t"
			mail_from = DEFAULT_FROM_EMAIL
			mail_to =  [form.cleaned_data['email']]
			
			qrc_image = qrcode.make(generated_qrc)
			qrc_image.save('site_media/'+ generated_qrc + ".png")
			msg = EmailMultiAlternatives(mail_subject, mail_body, mail_from, mail_to)
			msg.attach_file('site_media/'+ generated_qrc + ".png")
			msg.send()
			os.remove('site_media/'+ ticket.qr_code.qr_code + ".png")
			
			
			variables = RequestContext(request, {
				'ticket' : ticket
			})
			return render_to_response(
				'purchase/onthefly_success.html',
				variables
			)
	else:
		form = OnTheFlyTicketForm()
	variables = RequestContext(request, {
		'form' : form
	})
	return render_to_response(
		'main_page.html',
		variables
	)


def logout_page(request):
	logout(request)
	return HttpResponseRedirect('/')

@login_required
def user_page(request):
	user = request.user
	
	tickets = user.ticket_set.all()
	passes = user.pass_set.all()
	
	template = get_template('user_page.html')
	variables = RequestContext(request, {
		'username' : user.username,
		'tickets' : tickets,
		'passes' : passes
	})
	return render_to_response('user_page.html', variables)

def register_page(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = User.objects.create_user(
				username = form.cleaned_data['username'],
				password = form.cleaned_data['password1'],
				email = form.cleaned_data['email']
			)
			return HttpResponseRedirect('/register/success/')
	else:
		form = RegistrationForm()
	variables = RequestContext(request, {
		'form' : form
	})
	return render_to_response(
		'registration/register.html',
		variables
	)

def generate_qrcode(request, qr_code):
	response = HttpResponse(mimetype = "image/png")
	qrc_image = qrcode.make(qr_code)
	qrc_image.save(response, "PNG")
	return response