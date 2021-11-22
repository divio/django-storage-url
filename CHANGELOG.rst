=========
CHANGELOG
=========

0.8.1 (2021-11-22)
==================

* Fix issue with Azure account keys vs token credential.


0.8.0 (2021-11-19)
==================

* Added support for Azure account keys on top of SAS tokens.


0.7.0 (2021-09-06)
==================

* Dropped support for Python 3.5.
* Added support for Django 3.2.
* Added support for ``querystring_auth`` to the S3 backend.
* Fixed a compatibility issue with newer azure backends.


0.6.0 (2020-09-01)
==================

* Added support for Django 3.1.
* Dropped support for Python 2.7 and Python 3.4.
* Dropped support for Django < 2.2.
* Changed ``default_acl`` to ``object_parameters``.


0.5.0 (2020-05-28)
==================

 * Simplify AZ backend now that django-storages supports SAS tokens for Azure.
 * Support ACLs and custom container names.


0.4.0 (2018-12-06)
==================

* Extracting `region_name` from the DSN for S3.


0.3.0 (2018-11-23)
==================

* Expose `get_storage` as a top-level attribute.


0.2.1 (2018-11-02)
==================

* Fix an issue with Azure and custom domains.


0.2.0 (2018-11-01)
==================

* Initial Azure storage support.


0.1.0 (2018-10-31)
==================

* Initial release.
