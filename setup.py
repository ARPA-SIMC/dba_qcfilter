import os
import re

from setuptools import find_packages, setup



def get_version(package):
    # Thanks to Tom Christie
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


setup(
    name="dba_qcfilter",
    version=get_version("dba_qcfilter"),
    packages=find_packages(include=["dba_qcfilter"]),
    include_package_data=True,
    license='GPLv2+',
    description='QC filter for generic BUFR data',
    long_description='QC filter for generic BUFR data',
    url='http://github.com/arpa-simc/dba_qcfilter',
    author='Emanuele Di Giacomo',
    author_email="edigiacomo@arpae.it",
    test_suite="tests.runtests",
    entry_points={
        "console_scripts": {
            "dba_qcfilter = dba_qcfilter.cli.main",
        },
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
