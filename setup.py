
from __future__ import with_statement

# http://docs.python.org/distutils/
# http://packages.python.org/distribute/
try:
    from setuptools import setup
except:
    from distutils.core import setup

from setuptools.command.test import test as TestCommand

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        raise SystemExit(errno)

import os.path

version_py = os.path.join(os.path.dirname(__file__), 'ivi', 'version.py')
with open(version_py, 'r') as f:
    d = dict()
    exec(f.read(), d)
    version = d['__version__']

setup(
    name = 'python-ivi',
    description = 'Python Interchangeable Virtual Instrument Library',
    version = version,
    long_description = '''This package is a Python-based interpretation of the
Interchangeable Virtual Instrument standard, a software abstraction for
electronic test equipment that is remotely controllable.''',
    author = 'Alex Forencich',
    author_email = 'alex@alexforencich.com',
    url = 'http://alexforencich.com/wiki/en/python-ivi/start',
    download_url = 'http://github.com/python-ivi/python-ivi/tarball/master',
    keywords = 'IVI measurement instrument',
    license = 'MIT License',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Hardware :: Hardware Drivers',
        'Topic :: System :: Networking',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3'
        ],
    packages = ['ivi',
                'ivi.interface',
                'ivi.extra',
                'ivi.scpi',
                'ivi.agilent',
                'ivi.chroma',
                'ivi.colby',
                'ivi.dicon',
                'ivi.ics',
                'ivi.jdsu',
                'ivi.keithley',
                'ivi.lecroy',
                'ivi.rigol',
                'ivi.tektronix',
                'ivi.testequity'],
    requires = ['numpy'],
    extras_require = {
        'vxi11': ['python-vxi11'],
        'usbtmc': ['python-usbtmc'],
        'serial': ['pyserial']
    },
    tests_require = ['pytest'],
    cmdclass = {'test': PyTest}
)

