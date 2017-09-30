from setuptools import setup

setup(name='hypixel',
      version='0.4.0',
      description='This is a simple, unofficial library for getting values from the public Hypixel-API in Python.',
      url='https://github.com/SnuggIes/hypixel.py',
      author='Snuggle',
      author_email='snuggle@sprinkly.net',
      install_requires=['requests'],
      py_modules = ['hypixel', 'leveling'],
      python_requires='>=3',
      zip_safe=False)