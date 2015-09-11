from setuptools import setup
import codecs
import os

import flask_trace

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the relevant file
with codecs.open('README.rst', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="flask_trace",
    version=flask_trace.__version__,

    description="Log trace decorator function for Flask",
    long_description=long_description,

    # The project URL.
    url='https://github.com/canassa/flask-trace',

    # Author details
    author='Cesar Canassa',
    author_email='cesar@canassa.com',

    # Choose your license
    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',

        # Who the project is intended for.
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: User Interfaces',
        'Topic :: Utilities',

        'License :: OSI Approved :: MIT License',

        # Supported Python versions.
        'Programming Language :: Python :: 2.7',
    ],
    keywords='flask log trace logging',
    packages=['flask_trace'],
)
