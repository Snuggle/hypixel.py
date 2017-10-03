from setuptools import setup

setup(name='hypixel',
      version='0.4.1',
      description='This is a simple, unofficial library for getting values from the public Hypixel-API in Python.',
      url='https://github.com/SnuggIes/hypixel.py',
      author='Snuggle',
      author_email='snuggle@sprinkly.net',
      install_requires=['requests'],
      py_modules = ['hypixel', 'leveling'],
      python_requires='>=3',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.6',
        'Topic :: Games/Entertainment',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
      ]
)