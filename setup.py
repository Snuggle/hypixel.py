from setuptools import setup

with open('README.rst') as f:
    readme_content = f.read().strip()

with open('hypixel.py') as f:
    for line in f:
        if line.strip().startswith('__version__'):
            version = line.split('=')[1].strip().replace('"', '').replace("'", '')

setup(name='hypixel',
      include_package_data=True,
      keywords=["hypixel hypixel-api hypixel.py"],
      version=version,
      description='This is a simple, unofficial library for getting values from the public Hypixel-API in Python.',
      long_description=readme_content,
      url='https://github.com/SnuggIes/hypixel.py',
      author='Snuggle',
      author_email='snuggle@sprinkly.net',
      install_requires=['requests'],
      py_modules = ['hypixel', 'leveling'],
      python_requires='>=3.3',
      classifiers=[
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Games/Entertainment',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
      ]
)