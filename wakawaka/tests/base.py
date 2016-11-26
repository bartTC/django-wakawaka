from __future__ import unicode_literals

from django import get_version
from django.contrib.auth.models import User
from django.test import testcases
from distutils.version import StrictVersion

from wakawaka.models import WikiPage, Revision

DJANGO_VERSION = get_version()

class BaseTestCase(testcases.TestCase):
    """
    General integrity tests around the project.
    """
    def _create_user(self, username, password):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = User.objects.create(
                username=username, email='{}@example.com'.format(username))
            user.set_password(password)
        return user

    def login_superuser(self, create=True):
        username, password = 'superuser', 'foobar'
        user = self._create_user(username, password)
        user.is_superuser= True
        user.is_staff = True
        user.save()
        self.client.login(username=username, password=password)
        return user

    def login_staffuser_noperm(self, create=True):
        username, password = 'staffuser', 'foobar'
        user = self._create_user(username, password)
        user.is_staff = True
        user.save()
        self.client.login(username=username, password=password)
        return user

    def is_django_18(self):
        """
        :return bool: Whether the current Django version is <= 1.8
        """
        return StrictVersion(DJANGO_VERSION) <= StrictVersion('1.8')

    def create_wikipage(self, slug, title=None, content=None):
        """
        Manualy create a valid Wikipge with one Revision
        """
        title = title or '{} Page'.format(slug)
        content = content or 'Lorem ipsum {} page.'.format(slug)
        page = WikiPage.objects.create(slug=slug)
        Revision.objects.create(
            page = page,
            title=title,
            content=content,
            message='Created via API',
            creator_ip='127.0.0.1'
        )
        return page
