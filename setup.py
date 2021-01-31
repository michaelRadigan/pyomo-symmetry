from setuptools import setup
import os
import sys

_here = os.path.abspath(os.path.dirname(__file__))

version = {}
with open(os.path.join(_here, 'pyomo_symmetry', 'version.py')) as f:
    exec(f.read(), version)


install_requires = ['pyomo', 'pynauty-nice']

setup(
    name='pyomo-symmetry',
    version=version['__version__'],
    description='A (work in progress) module to find the symmetry groups of a pyomo model using a novel algorithm',
    author='Michael Radigan',
    author_email='michael@radigan.co.uk',
    url='https://github.com/michaelRadigan/pyomo-symmetry',
    license='Apache2.0',
    packages=['pyomo_symmetry'],
    install_requires=install_requires,
    include_package_data=True,
    classifiers=[],
)