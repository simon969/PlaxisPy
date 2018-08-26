from setuptools import setup, find_packages
import sys
if len(sys.argv) == 1:
    sys.argv.append('install')
    sys.argv.append(r'--user')

try:
    from setuptools import setup
except:
    from distutils.core import setup

setup(
    name="getPlaxisResults",
    version="0.1.0",
    packages=find_packages(),
    scripts=['getPlaxisResults.py']
)