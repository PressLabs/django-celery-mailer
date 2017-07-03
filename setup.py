#!/usr/bin/env python
import os
import sys

from celery_mailer import __version__
from setuptools import setup

# Work around setuptools bug
# http://article.gmane.org/gmane.comp.python.peak/2509
import multiprocessing

def publish():
    """Publish to Pypi"""
    os.system("python setup.py sdist upload")

if sys.argv[-1] == "publish":
    publish()
    sys.exit()

setup(
    name='django-celery-mailer',
    version=__version__,
    description='Django email backend that utilizes Celery for task execution.',
    long_description=open('README.md').read(),
    author='Funkbit',
    author_email='post@funkbit.no',
    url='https://github.com/funkbit/django-celery-mailer',
    license='BSD',
    packages=['celery_mailer'],
    install_requires=[
        'celery',
    ],
    tests_require=[
        'django',
    ],
    classifiers=(
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    )
)
