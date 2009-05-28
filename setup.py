from setuptools import setup, find_packages

setup(
    name='django-wakawaka',
    version='0.1',
    description='A super simple wiki app written in Python using the Django Framwork',
    long_description=open('README.rst').read(),
    author='Martin Mahner',
    author_email='martin@mahner.org',
    url='http://github.com/bartTC/django-wakawaka/tree/master',
    packages=find_packages('src', exclude=('wakawaka_project',)),
    package_dir = {'': 'src'},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    package_data = {
        'wakawaka': [
            'templates/wakawaka/*.html',
        ]
    },
    zip_safe=False,
)
