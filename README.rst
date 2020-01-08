.. image:: https://badge.fury.io/py/django-wakawaka.svg
    :target: https://badge.fury.io/py/django-wakawaka

.. image:: https://travis-ci.org/bartTC/django-wakawaka.svg?branch=master
    :target: https://travis-ci.org/bartTC/django-wakawaka

.. image:: https://api.codacy.com/project/badge/Grade/6f08231f5cd94c37a08c63946d9b42ba
    :alt: Codacy Badge
    :target: https://app.codacy.com/app/bartTC/django-wakawaka

.. image:: https://api.codacy.com/project/badge/Coverage/3fc9f0077122402ab3264978b994ecb8
    :target: https://www.codacy.com/app/bartTC/django-wakawaka


===============
django-wakawaka
===============

django-wakawaka is a super simple wiki system written in Python using the
Django framework.

* Links between Wiki pages are automatically resolved by their CamelCase naming
  scheme.

* It automatically keeps track of revision changes of a Page, while
  providing the ability to revert to earlier states.

* It also has a quite comprehensive permission integration, taking care of
  Django's default create/edit/delete permissions.

* Wakawaka is an application and indented to be placed in an existing project.

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

That's all. Wakawaka has no other dependencies than Django 1.11 or later.


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


Attachments:
============

Wakawaka does not provide the ability to store file attachments to wiki pages.
To do so, have a look on the side project `django-attachments`_ which provides
a unobstrusive way to add attachments to models.


Testing and Development:
========================

The project comes with a test library which can be simply invoked by Tox,
which tests the project under all current Python and Django versions::

    $ pip install tox
    $ tox

To run the testsuite manually in your development environment, install the
project using pipenv_::

    $ pipenv install
    $ pipenv run tests


Example Project:
================

The application comes with a sample project. This gives you a brief overview
about the Wiki features, and can help you with the integration of the
application into an existing project. It's alo used for the test suite::

    $ pipenv install
    $ pipenv run ./manage.py migrate
    $ pipenv run ./manage.py createsuperuser
    $ pipenv run ./manage.py runserver

.. _django-attachments: https://github.com/bartTC/django-attachments
.. _pipenv: https://pipenv.readthedocs.io/
