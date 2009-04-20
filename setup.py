from setuptools import setup, find_packages
import os

version = '0.2.4'

setup(name='tgext.admin',
      version=version,
      description="Admin Controller add-on for basic TG identity model.",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='TG2, TG, sprox, Rest, internet, adminn',
      author='Christopher Perkins',
      author_email='chris@percious.com',
      url='tgtools.googlecode.com',
      license='MIT',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['tgext'],
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'setuptools',
          'tgext.crud>=0.2.1',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
