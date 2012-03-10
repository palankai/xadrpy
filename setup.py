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
    version=read('VERSION').strip(),
    description="Django tool",
    long_description=read('README.rst'),
    classifiers=[
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Development Status :: Beta',
        'Intended Audience :: Developers',
        'Topic :: Tools',
    ],
    keywords=('django'),
    author='xadrpy Contributors',
    author_email='csaba.palankai@gmail.com',
    maintainer = 'Csaba Palankai',
    maintainer_email = 'csaba.palankai@gmail.com',
    url='https://github.com/pacsee/xadrpy',
    license='GNU LGPL',
    zip_safe=False,
    install_requires=[
        'Django==1.3.1',
    ],)
