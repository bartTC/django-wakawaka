.. image:: https://badge.fury.io/py/django-wakawaka.svg
    :target: https://badge.fury.io/py/django-wakawaka
    
.. image:: https://travis-ci.org/bartTC/django-wakawaka.svg?branch=master
    :target: https://travis-ci.org/bartTC/django-wakawaka

.. image:: https://codecov.io/github/bartTC/django-wakawaka/coverage.svg?branch=master
    :target: https://codecov.io/github/bartTC/django-wakawaka?branch=master

===============
django-wakawaka
===============

django-wakawaka is a super simple wiki system written in Python using the Django
framework.

* Links between Wiki pages are automatically resolved by their CamelCase naming
  scheme.

* It automatically keeps track of revision changes of a Page, while
  providing the ability to revert to earlier states.

* It also has a quite comprehensive permission integration, taking care of
  Django's default create/edit/delete permissions.

* Wakawaka can be used as an application on its own, or included into an existing
  project.

Some screenshots from the *Example Project*:

* `WikiIndex Page`_
* `Revision List`_
* `Page History`_
* `Page List`_

.. _WikiIndex Page: https://github.com/bartTC/django-wakawaka/raw/master/docs/_static/overview.png
.. _Revision List: https://github.com/bartTC/django-wakawaka/raw/master/docs/_static/revisions.png
.. _Page History: https://github.com/bartTC/django-wakawaka/raw/master/docs/_static/history.png
.. _Page List: https://github.com/bartTC/django-wakawaka/raw/master/docs/_static/pagelist.png

Installation:
=============

1. Put ``wakawaka`` to your INSTALLED_APPS in your settings.py within your
   django project.
2. Add ``(r'^wiki/', include('wakawaka.urls')),`` to your urls.py.

That's all. Wakawaka has no other dependencies than Django 1.8 or later.

**Private wiki:** If you want to deploy a private wiki so that every page
needs an login simply add this line ``(r'^wiki/', include('wakawaka.urls.authenticated')),``
to your urls.py instead of the above.


Configuration:
==============

Wakawaka takes care of Django's permission system. Grant your users always a
pair of ``wikipage`` and ``revision`` permissions either what they should do.
(Adding, changing or deleting WikiPages)

Optional Settings:
------------------

The name of your first wiki page is defined as ``WikiIndex``. You can change
this by adding a setting ``WAKAWAKA_DEFAULT_INDEX`` to your settings.py.
Example::

    WAKAWAKA_DEFAULT_INDEX = 'Home'

Words that are written in CamelCase (a pair of one upper letter followed by
*n* lower letters) are automatically treated as internal wiki links. You can
change this behaviour by adding a setting ``WAKAWAKA_SLUG_REGEX`` to your
settings.py. This holds a regular expression of the wiki name format. Default::

    WAKAWAKA_SLUG_REGEX = r'((([A-Z]+[a-z]+){2,})(/([A-Z]+[a-z]+){2,})*)'

To add markdown (or reStructuredText) support you can specify a function to
pass page content to before displaying it on the page. For example::

    import markdown
    WAKAWAKA_PREPROCESS_CONTENT_FUNCTION = markdown.markdown

``WAKAWAKA_PREPROCESS_CONTENT_FUNCTION`` can be any python callable that takes
a string and returns a string. It is applied before creating the internal wiki
links.

Attachments:
============

Wakawaka does not provide the ability to store file attachments to wiki pages.
To do so, have a look on the side project `django-attachments`_ which provides
a unobstrusive way to add attachments to models.


Testing and Development:
========================

The project comes with a (not so) comprehensive test library which can be
simply invoked by Tox, which tests the project under all current Python and
Djanog versions::

    $ pip install tox
    $ tox

To run the testsuite manually in your development environment, install the
project in a separate virtualenv. I'm using virtualenvwrapper_ here::

    $ mkvirtualenv --python=`which python3` wakawaka-env
    $ pip install -e .
    $ ./runtests.py


Example Project:
================

The application comes with a sample project. This gives you a brief overview
about the Wiki features, and can help you with the integration of the
application into an existing project. It's alo used for the test suite::

    $ mkvirtualenv --python=`which python3` wakawaka-env
    $ pip install -e .
    $ ./runtestproject.py migrate
    $ ./runtestproject.py createsuperuser
    $ ./runtestproject.py runserver

.. note:: ``runtestproject.py`` is the pendant to a regular ``manage.py`` file
    in a Django project..

.. _virtualenvwrapper: https://virtualenvwrapper.readthedocs.io/en/latest/
