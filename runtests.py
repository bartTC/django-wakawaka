#!/usr/bin/env python
import sys
import os

from django import setup
from django.conf import settings
from django.test.runner import DiscoverRunner

from wakawaka.tests.test_project import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wakawaka.tests.test_project.settings")


def runtests(*test_args):
    setup()
    test_runner = DiscoverRunner(verbosity=1)
    failures = test_runner.run_tests(['wakawaka'])
    if failures:
        sys.exit(failures)


if __name__ == '__main__':
    runtests(*sys.argv[1:])
