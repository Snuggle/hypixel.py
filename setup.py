import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

with open('./docs/README.rst') as f:
    readme_content = f.read().strip()

with open('hypixel.py') as f:
    for line in f:
        if line.strip().startswith('__version__'):
            version = line.split('=')[1].strip().replace('"', '').replace("'", '')

on_rtd = os.getenv('READTHEDOCS') == 'True'

requirements = []
with open('requirements.txt') as f:
  requirements = f.read().splitlines()

if on_rtd:
  requirements.append('sphinxcontrib-napoleon')

here = os.path.abspath(os.path.dirname(__file__))

class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPi via Twine…')
        os.system('twine upload dist/*')
        self.status('Finished uploading to PyPi! Cleaning up.')
        foldersToRemove = ['dist', 'build', 'hypixel.egg-info', '__pycache__']
        for folder in foldersToRemove:
            try:
                rmtree(os.path.join(here, folder))
            except OSError:
                pass

        sys.exit()

setup(name='hypixel',
      include_package_data=True,
      keywords=["hypixel hypixel-api hypixel.py"],
      version=version,
      description='This is a simple, unofficial library for getting values from the public Hypixel-API in Python.',
      long_description=readme_content,
      url='https://gitlab.com/Snuggie/hypixel.py',
      author='Snuggle',
      author_email='snuggle@sprinkly.net',
      install_requires=requirements,
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
     ],
    # $ setup.py publish support.
    cmdclass={
        'upload': UploadCommand,
    },
)