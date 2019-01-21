==========
Changelog:
==========

v1.1 (2019-01-21):

- Django 2.1 compatibility and and further cleanup.
- Dropped support for Django <v1.11.
- Dropped "authenticated" url patterns which were not functional since a while.

v1.0 (2016-11-26):

- Django 1.10 compatibility and total cleanup.
- Full Python 3 compatibility.
- Removed Pinax Group support.
- Tests.

v0.3: (2009-08-06):

- If a wikipage was not found, the view now raises a proper Http404 instead of a
  (silent) HttpResponseNotFound. This gives you the ability to display a proper
  404 page.
- All templates are now translatable using gettext.

v0.2 (2009-07-22):

- Edit-forms are now replaceable

.. _`django-attachments`: http://github.com/bartTC/django-attachments/
