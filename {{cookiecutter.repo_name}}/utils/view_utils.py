from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.template import TemplateDoesNotExist
from django import http
from django.conf import settings as dj_settings
from django.core.urlresolvers import reverse, resolve
from django.db.models import Q
from django.http import HttpResponse
from django.template import loader, RequestContext, Context
from django.utils.datastructures import SortedDict
from django.utils.safestring import mark_safe
from django.template import Template,Context
from django.template.loader import render_to_string


def build_template_from_string(template_string, params):
	return Template(template_string).render(Context(params))

def custom_render(request, *args, **kwargs):
	kwargs['context_instance'] = RequestContext(request)
	return render_to_response(*args, **kwargs)
	