pylw
======
Python Lightweight Webframework.

Usage
~~~~~~~
Please see main.py on |Git Hub| for usage details.

|Build Status|

This is a somewhat useful web framework.

It's meant to be fast, and to do very little.

It works with WSGI servers.

Features
~~~~~~~~~~
URL Routing, Cookies, Cookie signing (with itsdangerous), Allows headers to be
easily added, adds cookies and content length to headers automatically when
the response is returned.

No template engine is supplied, no ORM, no 'session' handling.  That's up to the
dev.  This framework handles the most basic of tasks.

Unicode support...none.
~~~~~~~~~~~~
We also don't support python3 at this time.  Unicode may or may not work for
you, I honestly don't know.  If it doesn't impact performance much, it might be
added in the future.

Complexity...zero.
~~~~~~~~~~~~

Some C code has been included to speed up query parsing and URL routing.

The C code for query parsing is much faster than the corresponding Python code,
however it does not support URL encoded characters, just strings.  Since I
anticipate the vast majority of GET requests to not use non-alphanumeric
characters, it's not high on my priority list.  The characters don't seem to
crash the software or cause problems, but they will just appear as-is instead
of decoded.

Cython support
~~~~~~~~~~~~
If you have Cython installed, this package will compile modules into C code.
This improves performance greatly, especially when using CRouter for URL
routing.


.. |Build Status| image:: https://travis-ci.org/michaelgugino/pylw.svg?branch=master
   :target: https://travis-ci.org/michaelgugino/pylw

.. |Git Hub| https://travis-ci.org/michaelgugino/pylw.svg?branch=master
      :target: https://travis-ci.org/michaelgugino/pylw
