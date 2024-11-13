#!/usr/bin/env python

from setuptools import setup


setup(
    name='libetrv',
    packages=['libetrv', 'libetrv.fields'],
    version='0.6.0',
    license='Apache License 2.0',
    description='Monitor and control your eTRV from Python',
    author='Adam Strojek',
    author_email='adam@strojek.info',
    url='https://github.com/AdamStrojek/libetrv',
    download_url='https://github.com/AdamStrojek/libetrv/archive/v0.4.1.tar.gz',
    keywords=['danfoss', 'etrv', 'libetrv'],
    install_requires=['fire', 'bluepy', 'xxtea', 'loguru', 'cstruct'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
