# Copyright 2015 Michael Gugino
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup
from setuptools import setup, find_packages, Extension
from setuptools.command.test import test as TestCommand
import sys, io

module1 = Extension('pylw.qs_parse', sources = ['pylw/qs_parse.c'])
module2 = Extension('pylw.route_find', sources = ['pylw/route_find.c'])

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
      long_description=io.open('README.rst', 'r', encoding='utf-8').read(),
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Web Environment',
          'Natural Language :: English',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: Apache Software License',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Topic :: Internet :: WWW/HTTP :: WSGI',
          'Topic :: Software Development :: Libraries :: Application Frameworks',
          'Programming Language :: Python',
          'Programming Language :: Python :: Implementation :: CPython',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: C',
      ],
      url='http://github.com/michaelgugino/pylw',
      author='Michael Gugino',
      author_email='mike@funwithlinux.net',
      tests_require=['pytest'],
      cmdclass={'test': PyTest},
      license='Apache',
      packages=['pylw'],
      ext_modules = [module1, module2],
      zip_safe=False)
