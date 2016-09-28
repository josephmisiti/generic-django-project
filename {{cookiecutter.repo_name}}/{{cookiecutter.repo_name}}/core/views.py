from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import requires_csrf_token

@requires_csrf_token
def page_404(request): 
	response = fetcher_render(request, '404.html')
	response.status_code = 404
	return response

@requires_csrf_token
def page_403(request): 
	response = fetcher_render(request, '403.html')
	response.status_code = 403
	return response

@requires_csrf_token
def page_500(request):
	response = fetcher_render(request, '500.html')
	response.fetcher_render = 500
	return response
