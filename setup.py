from setuptools import setup

setup(name='hypixel',
      include_package_data=True,
      keywords=["hypixel hypixel-api hypixel.py"],
      version='0.4.3',
      description='This is a simple, unofficial library for getting values from the public Hypixel-API in Python.',
      url='https://github.com/SnuggIes/hypixel.py',
      author='Snuggle',
      author_email='snuggle@sprinkly.net',
      install_requires=['requests'],
      py_modules = ['hypixel', 'leveling'],
      python_requires='>=3.3',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Games/Entertainment',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
      ]
)