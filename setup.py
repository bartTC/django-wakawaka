#!/usr/bin/env python
from setuptools import setup, find_packages

requirements = [
    'django>=1.8',
]

test_requirements = [
]

setup(
    name='django-wakawaka',
    version='1.0a',
    description='A super simple wiki app written in Python using the Django Framwork',
    long_description=open('README.rst').read(),
    author='Martin Mahner',
    author_email='martin@mahner.org',
    url='http://github.com/bartTC/django-wakawaka/',
    packages=find_packages(),
    package_data={
        'wakawaka/': [
            'static/*.*',
            'templates/*.*'
        ]
    },
    install_requires=requirements,
    tests_require=test_requirements,
    zip_safe=False,
)
