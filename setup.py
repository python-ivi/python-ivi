

# http://docs.python.org/distutils/
# http://packages.python.org/distribute/
try:
    from setuptools import setup
except:
    from distutils.core import setup

setup(
    name = 'pyivi',
    description = 'Python Interchangeable Virtual Instrument Library',
    version = '0.1',
    long_description = """A Python package for support of Interchangeable Virtual Instruments""",
    author = 'Alex Forencich',
    author_email = 'alex@alexforencich.com',
    url = 'http://github.com/alexforencich/pyivi',
    download_url = 'http://github.com/alexforencich/pyivi',
    keywords = 'IVI measurement instrument',
    license = 'MIT License',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'Topic :: System :: Hardware',
        'Programming Language :: Python 3'
        ],
    packages = ['pyivi', 'pyivi.agilent', 'pyivi.tektronix'],
    py_modules = ['ivi']
)

