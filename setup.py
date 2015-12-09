from setuptools import setup
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import sys

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

setup(name='pylw',
      version='0.1',
      description='The Python Lightweight Web Framework',
      url='http://github.com/michaelgugino/pylw',
      author='Michael Gugino',
      author_email='mike@funwithlinux.net',
      tests_require=['pytest'],
      cmdclass={'test': PyTest},
      license='GPLv3',
      packages=['pylw'],
      zip_safe=False)
