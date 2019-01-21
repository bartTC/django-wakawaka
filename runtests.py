#!/usr/bin/env python
import os
import sys

from django import setup
from django.test.runner import DiscoverRunner

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "wakawaka.tests.test_project.settings"
)


def runtests(*test_args):
    setup()
    test_runner = DiscoverRunner(verbosity=1)
    failures = test_runner.run_tests(['wakawaka'])
    if failures:
        sys.exit(failures)


if __name__ == '__main__':
    runtests(*sys.argv[1:])
