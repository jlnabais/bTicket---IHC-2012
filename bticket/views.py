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
from django.contrib.auth.views import password_reset
import datetime



# Create your views here.
def main_page(request):
	if request.method == 'POST':
		form = OnTheFlyTicketForm(request.POST)
		recovery_form = RecoveryOnTheFlyTicketForm(request.POST)
		trips_form = CheckNuberOfTripsForm(request.POST)
		ticket_form = BuyTicketForm(request.POST)
		
		if form.is_valid():
			generated_str = g.id_generator(10)
			while OnTheFlyTicket.objects.filter(recovery_code = generated_str).count():
				generated_str = g.id_generator(10)
			
			generated_qrc_str = g.id_generator(8)
			generated_qrc = hashlib.sha1('bticketcodeOTFT').hexdigest() + generated_qrc_str
			while OnTheFlyTicket.objects.filter(qr_code__qr_code = generated_qrc).count():
				generated_qrc_str = g.id_generator(8)
				generated_qrc = hashlib.sha1('bticketcodeOTFT').hexdigest() + generated_qrc_str
			
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
			
		if recovery_form.is_valid():
			try:
				ticket = OnTheFlyTicket.objects.get(recovery_code = recovery_form.cleaned_data['recovery_code'])
			except OnTheFlyTicket.DoesNotExist:
				form = OnTheFlyTicketForm()
				recovery_form = RecoveryOnTheFlyTicketForm()
				trips_form = CheckNuberOfTripsForm()
				ticket_form = BuyTicketForm()
				error_msg = 'There\'s no ticket associated with that recovery code.'
				variables = RequestContext(request, {
					'form' : form,
					'recovery_form': recovery_form,
					'trips_form' : trips_form,
					'error_msg' : error_msg
				})
				return render_to_response(
					'main_page.html',
					variables
				)
				
			form = SentEmailFromRecoveryForm()
			variables = RequestContext(request, {
				'ticket' : ticket,
				'form' : form
			})
			return render_to_response(
				'recovery/onthefly_recovery_success.html',
				variables
			)
			
		if trips_form.is_valid():
			try:
				ticket = OnTheFlyTicket.objects.get(recovery_code = trips_form.cleaned_data['code'])
			except OnTheFlyTicket.DoesNotExist:
				form = OnTheFlyTicketForm()
				recovery_form = RecoveryOnTheFlyTicketForm()
				trips_form = CheckNuberOfTripsForm()
				ticket_form = BuyTicketForm()
				error_msg_trips = 'There\'s no ticket associated with that recovery code.'
				variables = RequestContext(request, {
					'form' : form,
					'recovery_form': recovery_form,
					'trips_form' : trips_form,
					'error_msg_trips' : error_msg_trips
				})
				return render_to_response(
					'main_page.html',
					variables
				)
				
			form = OnTheFlyTicketForm()
			recovery_form = RecoveryOnTheFlyTicketForm()
			trips_form = CheckNuberOfTripsForm()
			ticket_form = BuyTicketForm()
			trips = ticket.number_of_trips
			variables = RequestContext(request, {
				'ticket' : ticket,
				'form' : form,
				'recovery_form': recovery_form,
				'trips_form' : trips_form,
				'trips' : trips
			})
			return render_to_response(
				'main_page.html',
				variables
			)
			
		if ticket_form.is_valid():
			n_trips = ticket_form.cleaned_data['number_of_trips']
			
			generated_qrc_str = g.id_generator(8)
			generated_qrc = hashlib.sha1('bticketcodeTicket').hexdigest() + generated_qrc_str
			while OnTheFlyTicket.objects.filter(qr_code__qr_code = generated_qrc).count():
				generated_qrc_str = g.id_generator(8)
				generated_qrc = hashlib.sha1('bticketcodeTicket').hexdigest() + generated_qrc_str
			
			qrcode_obj = QRCode.objects.create(qr_code = generated_qrc)
			
			Ticket.objects.create(user = UserProfile.objects.get(user = request.user), qr_code = qrcode_obj, emission_date = datetime.datetime.now(), number_of_trips = n_trips)
			
			mail_subject = 'bTicket|OntheFly Purchase'
			mail_body = 'Ticket information: \n\n \tUser: '+ request.user.username +'\n \tNumber of trips: '+ str(n_trips) +'\n\tQR Code:\n\t'
			mail_from = DEFAULT_FROM_EMAIL
			mail_to =  [UserProfile.objects.get(user = request.user).user.email]
			
			qrc_image = qrcode.make(generated_qrc)
			qrc_image.save('site_media/'+ generated_qrc + ".png")
			msg = EmailMultiAlternatives(mail_subject, mail_body, mail_from, mail_to)
			msg.attach_file('site_media/'+ generated_qrc + ".png")
			msg.send()
			os.remove('site_media/'+ generated_qrc + ".png")
			
			msg = "Ticket succefully bought!"
			form = OnTheFlyTicketForm()
			recovery_form = RecoveryOnTheFlyTicketForm()
			trips_form = CheckNuberOfTripsForm()
			ticket_form = BuyTicketForm()
			variables = RequestContext(request, {
				'form' : form,
				'recovery_form': recovery_form,
				'trips_form' : trips_form,
				'ticket_form' : ticket_form,
				'ticket_purchase_msg' : msg
			})
			return render_to_response(
				'main_page.html',
				variables
			)
			
	else:
		form = OnTheFlyTicketForm()
		recovery_form = RecoveryOnTheFlyTicketForm()
		trips_form = CheckNuberOfTripsForm()
		ticket_form = BuyTicketForm()
		variables = RequestContext(request, {
			'form' : form,
			'recovery_form': recovery_form,
			'trips_form' : trips_form,
			'ticket_form' : ticket_form
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
	userp = UserProfile.objects.get(user = request.user)
	
	tickets = userp.ticket_set.all()
	passes = userp.pass_set.all()
	image = userp.avatar
	#template = get_template('user_page.html')
	
	variables = RequestContext(request, {
		'username' : userp.user.username,
		'tickets' : tickets,
		'passes' : passes,
		'image' : image,
		'full_name' : userp.user.get_full_name()
	})
	return render_to_response('user_page.html', variables)

@login_required
def manage_page(request):
	if request.method == 'POST':
		userp = UserProfile.objects.get(user = request.user)
		form = UserProfileManagementForm(request.POST, request.FILES, instance = request.user.userprofile)
		if form.is_valid():
			user = request.user
			user.email = form.cleaned_data['email']
			user.first_name = form.cleaned_data['first_name']
			user.last_name = form.cleaned_data['last_name']
			user.save()
			
			if form.cleaned_data['avatar']:
				userp.avatar.save(form.cleaned_data['avatar'].name, form.cleaned_data['avatar'], save = True)
			
			msg = "Account info changed successfully"
				
			variables = RequestContext(request, {
				'form' : form,
				'msg' : msg
			})
			return render_to_response(
				'manage/manage.html',
				variables
			)
	else:
		form = UserProfileManagementForm(
			initial = { 'email': request.user.email, 'first_name': request.user.first_name, 'last_name': request.user.last_name, },
			instance = request.user.userprofile)
		variables = RequestContext(request, {
			'form' : form
		})
		return render_to_response(
			'manage/manage.html',
			variables
		)

def register_page(request):
	if request.method == 'POST':
		form = UserProfileRegistrationForm(request.POST, request.FILES)
		if form.is_valid():
			user = User.objects.create_user(
				username = form.cleaned_data['username'],
				password = form.cleaned_data['password1'],
				email = form.cleaned_data['email'],
			)
			user.first_name = form.cleaned_data['first_name']
			user.last_name = form.cleaned_data['last_name']
			user.save()
			avatar = form.cleaned_data['avatar']
			UserProfile.objects.create(user = user, avatar = avatar)
			return HttpResponseRedirect('/register/success/')
	else:
		form = UserProfileRegistrationForm()
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

def send_email_from_recovery(request, rcode):
	if request.method == 'POST':
		form = SentEmailFromRecoveryForm(request.POST)
		ticket = OnTheFlyTicket.objects.get(recovery_code = rcode)
		if form.is_valid():
			mail_subject = 'bTicket|OntheFly Recovery'
			mail_body = 'The following Ticket information was issued from our service to been sent to this e-mail.\n\nTicket information: \n\n \tRecovery Code:\n\t' +  ticket.recovery_code + "\n \tQR Code:\n\t"
			mail_from = DEFAULT_FROM_EMAIL
			mail_to =  [form.cleaned_data['email']]
		
			qrc_image = qrcode.make(ticket.qr_code.qr_code)
			qrc_image.save('site_media/'+ ticket.qr_code.qr_code + ".png")
			msg = EmailMultiAlternatives(mail_subject, mail_body, mail_from, mail_to)
			msg.attach_file('site_media/'+ ticket.qr_code.qr_code + ".png")
			msg.send()
			os.remove('site_media/'+ ticket.qr_code.qr_code + ".png")
		
			variables = RequestContext(request, {
				'email' : form.cleaned_data['email']
			})
			return render_to_response(
				'recovery/onthefly_recovery_success.html',
				variables
			)
	else:
		form = SentEmailFromRecoveryForm()
		variables = RequestContext(request, {
			'form' : form
		})
		return render_to_response(
			'recovery/onthefly_recovery_success.html',
			variables
		)
	