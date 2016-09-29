import re
import logging

from django.db import models
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, UserManager)
from django.core.urlresolvers import reverse
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save

from model_utils import Choices
from model_utils.models import TimeStampedModel

from rest_framework.authtoken.models import Token


logger = logging.getLogger(__name__)

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
        
        
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
