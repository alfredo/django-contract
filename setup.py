#!/usr/bin/env python
import os

from setuptools import setup, find_packages

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

setup(
    name='django_contract',
    version='0.1.0',
    description='API generator from RAML documentation',
    long_description=README,
    author='Alfredo Aguirre',
    author_email='hello@madewithbyt.es',
    license='BSD License',
    url='https://github.com/alfredo/',
    include_package_data=True,
    package_data={
        'django_contract': [],
    },
    zip_safe=False,
    scripts=[],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=find_packages(exclude=['tests']),
    dependency_links=[
        'https://github.com/an2deg/pyraml-parser/archive/master.zip#egg=pyraml-parser-0.1.5',
    ],
    install_requires=[
        'Django>=1.7',
        # 'pyraml-parser>=0.1.3',
    ],
)
