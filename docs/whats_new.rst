.. currentmodule:: hypixel

.. _whats_new:

What's New
============

This page shows what has changed in different versions of the API.

v0.6.5
--------
Implemented URL-by-URL caching. This makes everything suuuuper fast. It doesn't cache any key-requests and cleans the cache over time. The default caching time is 60 seconds, but you can change this by using ``hypixel.setCacheTime(60.0)``.

Cached single-requests usually take ~0.005s and non-cached single-requests take ~0.5s in basic tests.

v0.6.0
--------
Made all requests asynchronous! This has reduced the loading time of seven players, for example, from ~14s load time to ~5s load time.

v0.5.0
------
This is a pretty polished version now. Just a few things to clean-up and a few improvements.
It's relatively slow, though. The next minor version number, v0.6.x, will focus primarily on speed.

v0.4.0
------
Create Travis Ci tests and simplified use of the library.

**Old:**

.. code-block:: python
    
    variable = hypixel.Player('username').getJSON()
    print(variable.getLevel())
    >>> 96.3424329924
    print(variable.getJSON.JSON['networkExp'])
    >>> 4723883

**New:**

.. code-block:: python

    variable = hypixel.Player('username')
    print(variable.getLevel())
    >>> 96.3424329924
    print(variable.JSON['networkExp'])
    >>> 4723883