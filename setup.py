from setuptools import setup


setup(
    name='Flask-Cors',
    version='1.1.1',
    url='https://github.com/wcdolphin/flask-cors',
    license='MIT',
    author='Cory Dolphin',
    author_email='wcdolphin@gmail.com',
    description="A Flask extension adding a decorator for CORS support",
    long_description=__doc__,
    py_modules=['flask_cors'],
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
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)