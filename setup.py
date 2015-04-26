from setuptools import setup, find_packages
import os

version = '0.6.5'
here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.txt')).read()
    CHANGES = open(os.path.join(here, 'docs/HISTORY.txt')).read()
except IOError:
    README = CHANGES = ''

setup(name='tgext.admin',
      version=version,
      description="Admin Controller add-on for basic TG identity model.",
      long_description=README + "\n" +
                       CHANGES,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='turbogears2.extension, TG2, TG, sprox, Rest, internet, admin',
      author='Christopher Perkins',
      author_email='chris@percious.com',
      url='https://github.com/TurboGears/tgext.admin',
      license='MIT',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['tgext'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'tgext.crud>=0.7.1',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )

