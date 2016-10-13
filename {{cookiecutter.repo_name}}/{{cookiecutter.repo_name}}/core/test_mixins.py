from django.conf import settings
from django.utils import timezone

from faker import Faker

from {{cookiecutter.repo_name}}.accounts.models import User

fake = Faker()
fake.seed(9999999)

GENERIC_PASSWORD = 'mypassword'

class TestingMixin(object):

    @classmethod
    def create_user(self, **kwargs):
        """ create a user from thing air """
        ee = fake.free_email()
        email = kwargs.get('email', ee)
        first_name = kwargs.get('first_name',fake.first_name())
        last_name = kwargs.get('last_name',fake.last_name())

        user = User.objects.create(username=email,email=email)
        user.first_name = first_name
        user.last_name = last_name
        user.is_superuser = kwargs.get('is_superuser',False)
        user.is_staff = kwargs.get('is_staff',False)
        user.set_password(GENERIC_PASSWORD)
        user.save()
