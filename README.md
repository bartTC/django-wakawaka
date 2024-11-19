[![](https://badge.fury.io/py/django-wakawaka.svg)](https://badge.fury.io/py/django-wakawaka)

_Compatibility Matrix:_

| Py/Dj     | 3.9 | 3.10 | 3.11 | 3.12 | 3.13 |
| --------- | --- | ---- | ---- | ---- |------|
| 4.2 (LTS) | ✓   | ✓    | ✓    | ✓    | ✓    |
| 5.0       |     | ✓    | ✓    | ✓    | ✓    |
| 5.1       |     | ✓    | ✓    | ✓    | ✓    |

# django-wakawaka

django-wakawaka is a super simple wiki system written in Python using the
Django framework.

- Links between Wiki pages are automatically resolved by their CamelCase naming
  scheme.

- It automatically keeps track of revision changes of a Page, while
  providing the ability to revert to earlier states.

- It also has a quite comprehensive permission integration, taking care of
  Django's default create/edit/delete permissions.

- Wakawaka is an application and indented to be placed in an existing project.

Some screenshots from the _Example Project_:

- [WikiIndex Page][WikiIndex Page]
- [Revision List][Revision List]
- [Page History][Page History]
- [Page List][Page List]

[WikiIndex Page]: https://github.com/bartTC/django-wakawaka/raw/main/docs/_static/overview.png
[Revision List]: https://github.com/bartTC/django-wakawaka/raw/main/docs/_static/revisions.png
[Page History]: https://github.com/bartTC/django-wakawaka/raw/main/docs/_static/history.png
[Page List]: https://github.com/bartTC/django-wakawaka/raw/main/docs/_static/pagelist.png

## Installation:

1. Put `wakawaka` to your INSTALLED_APPS in your settings.py within your
   django project.
2. Add `(r'^wiki/', include('wakawaka.urls')),` to your urls.py.

That's all. Wakawaka has no other dependencies than Django 1.11 or later.

## Configuration:

Wakawaka takes care of Django's permission system. Grant your users always a
pair of `wikipage` and `revision` permissions either what they should do.
(Adding, changing or deleting WikiPages)

### Optional Settings:

The name of your first wiki page is defined as `WikiIndex`. You can change
this by adding a setting `WAKAWAKA_DEFAULT_INDEX` to your settings.py.
Example:

    WAKAWAKA_DEFAULT_INDEX = 'Home'

Words that are written in CamelCase (a pair of one upper letter followed by
_n_ lower letters) are automatically treated as internal wiki links. You can
change this behaviour by adding a setting `WAKAWAKA_SLUG_REGEX` to your
settings.py. This holds a regular expression of the wiki name format. Default:

    WAKAWAKA_SLUG_REGEX = r'((([A-Z]+[a-z]+){2,})(/([A-Z]+[a-z]+){2,})*)'

### Attachments:

Wakawaka does not provide the ability to store file attachments to wiki pages.
To do so, have a look on the side project [django-attachments][django-attachments]
which provides a unobstrusive way to add attachments to models.

## Testing and Development:

The project comes with a test library which can be simply invoked by Tox,
which tests the project under all current Python and Django versions:

    $ pip install tox
    $ tox

To run the testsuite manually in your development environment, install the
project using [Poetry][poetry]:

    $ poetry install
    $ pipenv run pytest

## Example Project:

The application comes with a sample project. This gives you a brief overview
about the Wiki features, and can help you with the integration of the
application into an existing project. It's alo used for the test suite:

    $ poetry install
    $ poetry run ./manage.py migrate
    $ poetry run ./manage.py createsuperuser
    $ poetry run ./manage.py runserver

[django-attachments]: https://github.com/bartTC/django-attachments
[poetry]: https://python-poetry.org
