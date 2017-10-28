.. currentmodule:: hypixel

.. about:


About
=====

This is a simple Python library which allows you to get values from the `Hypixel Public API <https://api.hypixel.net>`_.
With this library, you can get statistics and information from most things on the Hypixel Network.

It was created for free by `Snuggle <https://hypixel.net/player/Snuggle>`_, a volunteer-moderator for the network.

You should totally take a look at the `GitHub page <https://github.com/Snuggle/hypixel.py>`_, too!

.. _how_to_use:

Installation/Usage
------------------

You should use pip to install this library, using the following command: ``pip install hypixel``. If you're unsure how, please search for a good tutorial online.

Once hypixel.py is actually installed, you can type ``import hypixel`` at the top of your Python file to import the library. You should then be able to use ``hypixel.setKeys(['API_KEY_HERE'])`` to set your API key.

You can then do ``hypixel.Player('Snuggle')`` to create a Player-object and you can use any of the functions that are documented within the :doc:`api` or even take a look at some of the provided :doc:`examples`.

Project Idea
------------

I was developing a Discord bot for Hypixel and I was a massive fan of the Discord Python API I was using, `Discord.py <https://github.com/Rapptz/discord.py>`_. After a few days of creating this bot, I realised that a lot of the functions I was using could be used by other people. 

The original `Hypixel-bot <https://sprinkly.net/hypixelbot>`_ was a complete mess of spaghetti code, so I decided to split that project in twain. One project for all the Hypixel-related functions, hypixel.py, and a rewritten `Hypixel-bot <https://sprinkly.net/hypixelbot>`_ that actually uses the API.

I have taken a lot of inspiration from how `Discord.py <https://github.com/Rapptz/discord.py>`_ had organised their documentation and code, and started using it as a way to learn how to actually create something for people to use.

From this, I have learnt how to actually use GitHub, how to publish packages to `PyPi/pip <https://pypi.org/project/hypixel/>`_, how to use continuous integration testing with `Travis CI <https://travis-ci.com/SnuggIes/hypixel.py>`_, how to actually document code (Automatically, too!) and countless more things about Python as a language.

This is my first publically-released project, I'd love any feedback if you actually use this! ❤


Technical Details
------------------

This library sends simple GET requests to Hypixel's RESTful API and serves as an object-oriented wrapper for people developing in Python, and who wish to use Hypixel's API.
This comes with a simple implementation of caching and utilizes asynchronous requests.