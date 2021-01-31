from setuptools import setup
import os
import sys

_here = os.path.abspath(os.path.dirname(__file__))

version = {}
with open(os.path.join(_here, 'pyomo_mps', 'version.py')) as f:
    exec(f.read(), version)


install_requires = ['pyomo', 'pynauty-nice']

setup(
    name='pyomo-mps',
    version=version['__version__'],
    description='A (work in progress) module to find the symmetry groups of a pyomo model',
    author='Michael Radigan',
    author_email='michael@radigan.co.uk',
    url='https://github.com/michaelRadigan/pyomo-mps',
    license='Apache2.0',
    packages=['pyomo_mps'],
    install_requires=install_requires,
    test_requires=test_requires,
    include_package_data=True,
    classifiers=[],
)