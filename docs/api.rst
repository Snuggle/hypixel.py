.. currentmodule:: hypixel

.. api:



API Reference
===============

This section outlines the functions and methods that are available as part of `hypixel.py <https://github.com/Snuggle/hypixel.py>`_.

It is automatically generated and updated from the Docstrings present within the source.

.. note::

    This documentation is designed to be as easy to read and understand as
    possible. It aims to be a comprehensive reference for the API, but please
    note that there may be missing functions or methods.

Version Information
---------------------

There is one main way to get the version for this library.

.. data:: __version__
    
    Return the version number as a string. Example: ``'0.6.5'``

Miscellaneous Functions
------------------------

.. autofunction:: setKeys(api_keys)

.. autofunction:: setCacheTime(seconds)


Player
-------

.. autoclass:: Player
    :members:

Guild
-------

.. autoclass:: Guild
    :members:

Exceptions
-----------
.. autoexception:: HypixelAPIError
.. autoexception:: PlayerNotFoundException