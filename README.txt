Introduction
============

Changelog
===========

0.7.0
-----

* Improved template engine detection, didn't work well for unsupported engines. Now admin properly displays when using Kajiki
* Admin.make_controller is now a public method so that users can leverage it to create new CRUD controllers with Admin lookandfeel

0.6.6
-----
* Fix for allow_only not accepting custom predicated
* Preliminary support for Sprox version with subdocuments editing

0.6.0
------
Support for Layouts in TGAdminConfig with Bootstrap3 Layout

0.3
----
Lookup now uses ProviderSelector, for better mongo support

0.2.6
-----
Bugfix release.  Support for _method fields in TG2.1

0.2.5
------
* Addition of defaultCrudRestController to
CRCConfig allows one to customize the controller
that the admin uses.

* Fixes tgadminconfig to override the Password properly for Users
