from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import requires_csrf_token
from django.shortcuts import render

@requires_csrf_token
def page_404(request): 
	response = render(request, '404.html')
	response.render = 404
	return response

@requires_csrf_token
def page_403(request): 
	response = render(request, '403.html')
	response.render = 403
	return response

@requires_csrf_token
def page_500(request):
	response = render(request, '500.html')
	response.render = 500
	return response
