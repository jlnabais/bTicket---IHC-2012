from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import Context, RequestContext
from django.template.loader import get_template
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


# Create your views here.
def main_page(request):
	return render_to_response(
		'main_page.html', RequestContext(request)
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
	