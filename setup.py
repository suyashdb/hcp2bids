from setuptools import setup
import os, glob, shutil
import re, json, numpy
import nibabel as ni

here = os.path.abspath(os.path.dirname(__file__))

setup(
    name="hcp2bids",

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # http://packaging.python.org/en/latest/tutorial.html#version
    version='0.1.0',

    description="Command line tool to convert HCP dataset to a Brain Imaging Data Structure "
                "compatible dataset.",
    long_description="Command line tool to convert HCP dataset to a Brain Imaging Data Structure "
                     "compatible dataset.",

    # The project URL.
    url='https://github.com/suyashdb/hcp2bids',

    # Choose your license
    license='BSD',

    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: BSD License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
    ],

    # What does your project relate to?
    keywords='BIDS HCP NIH',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages.
    packages=["hcp2bids"],

    # List run-time dependencies here.  These will be installed by pip when your
    # project is installed.
    install_requires = ["numpy",
                        'nibabel'],

    include_package_data=True,

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'hcp2bids=hcp2bids.main:main',
        ],
    },
)
