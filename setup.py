#!/usr/bin/env python

from setuptools import setup, find_packages
import os
import sys
import codecs

def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='xadrpy',
    packages=find_packages('src'),
    package_dir={'':'src'},
    include_package_data=True,    
    version=read(os.path.join('src','xadrpy','VERSION')).strip(),
    description="Django tool",
    long_description='''Django and python tool with many useful packages, modules.''',
    classifiers=[
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Framework :: Django',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords=('django'),
    author='Csaba Palankai',
    author_email='csaba.palankai@gmail.com',
    maintainer = 'Csaba Palankai',
    maintainer_email = 'csaba.palankai@gmail.com',
    url='https://github.com/pacsee/xadrpy',
    license='GNU LGPL',
    zip_safe=False,
    scripts=['src/xadrpy/management/xcmd.py'],
    install_requires=[
    ],)
