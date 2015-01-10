import re

from django.db import models
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, UserManager)
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db.models import Q
from django.core.exceptions import PermissionDenied

from localflavor.us.us_states import US_STATES
US_STATES += ("INTL","International"),

import logging as log
logging = log.getLogger(__name__)

class User(AbstractBaseUser, PermissionsMixin):
	
	class Meta:
		app_label = 'accounts'
		db_table = "auth_user"

	username = models.CharField(_('username'), max_length=75, unique=True,
		help_text=_('Required. 30 characters or fewer. Letters, numbers and '
					'@/./+/-/_ characters'),
		validators=[
			validators.RegexValidator(re.compile('^[\w.@+-]+$'), _('Enter a valid username.'), 'invalid')
		])
	full_name = models.CharField(_('full name'), max_length=254, blank=True, help_text="Full name of the user")
	email = models.EmailField(_('email address'), max_length=254, unique=True)
	title = models.CharField(max_length=100, blank=True, help_text="Title of the user")
	phone = models.CharField(max_length=25, blank=True, help_text="Phone number of the user")
	company = models.CharField(max_length=100, blank=True, help_text="Company of the user")
	website = models.URLField(max_length=100, blank=True, help_text="Website of the user")
	street_1 = models.CharField(max_length=100, blank=True, help_text="Street of the user")
	street_2 = models.CharField(max_length=100, blank=True, help_text="APT/Building of the user")
	city = models.CharField(max_length=100, blank=True, help_text="City of the user")
	state = models.CharField(max_length=4, blank=True, choices=US_STATES, help_text="State of the user")
	country = models.CharField(max_length=50, blank=True, help_text="Country of the user")
	zipcode = models.CharField(max_length=25, blank=True, help_text="Zipcode name of the user")
	
	is_staff = models.BooleanField(_('staff status'), default=False,
		help_text=_('Designates whether the user can log into this admin '
					'site.'))
	is_active = models.BooleanField(_('active'), default=True,
		help_text=_('Designates whether this user should be treated as '
					'active. Unselect this instead of deleting accounts.'))
	date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
	
	password_hash = models.CharField(max_length=50,null=True,help_text="Forgot password hash")
		
	objects = UserManager()
	
	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']
	
	def get_full_name(self):
		return self.full_name

	def get_short_name(self):
		return self.username
