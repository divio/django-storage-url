#!/usr/bin/env python
from setuptools import find_packages, setup


# we need to declare the version here
__version__ = "0.6.0"


REQUIREMENTS = ["django>=2.2", "django-storages", "furl"]


CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "Environment :: Web Environment",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: BSD License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Framework :: Django",
    "Framework :: Django :: 2.2",
    "Framework :: Django :: 3.0",
    "Framework :: Django :: 3.1",
    "Topic :: Internet :: WWW/HTTP",
    "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    "Topic :: Software Development",
    "Topic :: Software Development :: Libraries",
]


setup(
    name="django-storage-url",
    version=__version__,
    author="Jonathan Stoppani",
    author_email="jonathan.stoppani@divio.com",
    url="https://github.com/divio/django-storage-url",
    license="MIT",
    description="URL-based Django storage configuration",
    long_description=open("README.rst").read(),
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=REQUIREMENTS,
    classifiers=CLASSIFIERS,
    test_suite="tests.settings.run",
)
