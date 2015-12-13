from setuptools import setup
from setuptools import setup, find_packages, Extension
from setuptools.command.test import test as TestCommand
import sys, io, os, glob

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

#Cython Support
try:
    from Cython.Distutils import build_ext
    CYTHON = True
except ImportError:
    CYTHON = False

if CYTHON:
    def list_modules(dirname):
        filenames = glob.glob(os.path.join(dirname, '*.py'))

        module_names = []
        for name in filenames:
            module, ext = os.path.splitext(os.path.basename(name))
            if module != '__init__':
                module_names.append(module)

        return module_names

    ext_modules = [
        Extension('pylw.' + ext, [os.path.join('pylw', ext + '.py')])
        for ext in list_modules(os.path.join('.', 'pylw'))]

    ext_modules.append(module1)
    ext_modules.append(module2)

    cmdclass = {'build_ext': build_ext, 'test': PyTest}

else:
    cmdclass = {'test': PyTest}
    ext_modules = [module1, module2]

setup(name='pylw',
      version='0.1.8',
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
          'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
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
      cmdclass=cmdclass,
      license='Apache',
      packages=['pylw'],
      ext_modules = ext_modules,
      zip_safe=False)
