from django.template import Library
from django.conf import settings

register = Library()

@register.simple_tag
def include_javascripts(asset_package):
	"""Prints out a template of <script> tags based on an asset package name."""
	asset_type = 'javascripts'
	return settings.JAMMIT.render_tags(asset_type, asset_package)

@register.simple_tag
def include_stylesheets(asset_package):
	"""Prints out a template of <link> tags based on an asset package name."""
	asset_type = 'stylesheets'
	return settings.JAMMIT.render_tags(asset_type, asset_package)