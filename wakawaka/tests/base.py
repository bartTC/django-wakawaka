
from django import get_version
from django.contrib.auth.models import User
from django.test import testcases

from wakawaka.models import Revision, WikiPage

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
                username=username,
                email=f"{username}@example.com",
            )
            user.set_password(password)
        return user

    def login_superuser(self, create=True):
        username, password = "superuser", "foobar"
        user = self._create_user(username, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        self.client.login(username=username, password=password)
        return user

    def login_staffuser_noperm(self, create=True):
        username, password = "staffuser", "foobar"
        user = self._create_user(username, password)
        user.is_staff = True
        user.save()
        self.client.login(username=username, password=password)
        return user

    def create_wikipage(self, slug, *args):
        """
        Creates a WikiPage using the given slug. Creates a Revision with the
        content of each additional argument. Example::

            >>> self.create_wikipage('WikiIndex', 'This is some content')

        Creates one Page WikiIndex with one Title/Text 'This is some content')

            >>> self.create_wikipage('WikiIndex', \
            'This is the first revision', 'This is the second revision')

        Creates one Page WikiIndex with two revisions, the first one and
        the second one later.
        """
        page = WikiPage.objects.create(slug=slug)
        for rev in args:
            Revision.objects.create(
                page=page,
                content=rev,
                message=f"Created via API: {rev}",
                creator_ip="127.0.0.1",
            )
        return page
