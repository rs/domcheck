Domcheck: Domain Ownership Validation
=====================================

.. image:: https://img.shields.io/pypi/v/domcheck.svg
    :target: https://pypi.python.org/pypi/domcheck

.. image:: https://travis-ci.org/rs/domcheck.svg?branch=master
    :target: https://travis-ci.org/rs/domcheck

This Python library implements different strategies to validate the ownership of a domain name.

Available strategies
--------------------

All strategies takes 3 arguments: the domain to check, a static DNS safe ``prefix`` like "yourservice-domain-verification" and a randomly generated ``code``.

- **DNS TXT record**: checks for the ``{prefix}-{code}`` string present in one of the ``TXT`` records on the domain name.
- **DNS CNAME record**: checks for the existence of ``CNAME` record composed on the static ``{prefix}-{code}`` on the domain pointing to domain (usually yours) which the host is {prefix} (i.e.: {prefix}.yourdomain.com). NOTE: you may want to make sure that {prefix}.yourdomain.com resolves to something as some zone editors may check that.
- **Meta Tag**: checks for the presence of a ``<meta name="{prefix}" content="{code}">`` tag in the ``<head>`` part of the domain's home page using either HTTP or HTTPs protocols.
- **HTML File**: checks for the presence of a file named ``{code}.html`` at the root of the domain's website containing the string ``{prefix}={code}`` using either HTTP or HTTPs protocols.

Usage Example
-------------

Simple usage will check the domain with all available strategies and return ``True`` if the validation passed:

.. code-block:: python

    import domcheck

    domain = "example.com"
    prefix = "myservice-domain-verification"
    code = "myserviceK2d8a0xdhh"

    if domcheck.check(domain, prefix, code):
        print("This domain is verified")


You may filter strategies by passing a coma separated list of strategies:

.. code-block:: python

    domcheck.check(domain, prefix, code, strategies="dns_txt,meta_tag")

Installation
------------

To install domcheck, simply:

    $ pip install domcheck

Licenses
--------

All source code is licensed under the `MIT License <https://raw.githubusercontent.com/rs/domcheck/master/LICENSE>`_.
