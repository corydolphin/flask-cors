# -*- coding: utf-8 -*-
"""
    Flask-CORS
    ~~~~~~~~~~

    Flask-CORS is a simple extension to Flask allowing you to support cross
    origin resource sharing (CORS) using a simple decorator.
"""

from setuptools import setup

from _version import __version__

setup(
    name='Flask-Cors',
    version=__version__,
    url='https://github.com/wcdolphin/flask-cors',
    license='MIT',
    author='Cory Dolphin',
    author_email='wcdolphin@gmail.com',
    description="A Flask extension adding a decorator for CORS support",
    long_description=open('README.rst').read(),
    py_modules=['flask_cors','_version'],
    # if you would be using a package instead use packages instead
    # of py_modules:
    # packages=['flask_sqlite3'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'Six'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
