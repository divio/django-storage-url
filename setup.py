from setuptools import setup, find_packages

setup(
    name="django-storage-url",
    version="0.4.0",
    packages=find_packages(),
    url="https://github.com/divio/django-storage-url",
    license="MIT",
    author="Jonathan Stoppani",
    author_email="jonathan.stoppani@divio.com",
    description="URL-based Django storage configuration",
    install_requires=["django-storages", "furl"],
    extras_require={},
    include_package_data=True,
)
