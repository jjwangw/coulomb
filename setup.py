import sys
from setuptools import setup, find_packages
with open('requirements.txt') as f:
     INSTALL_REQUIRES=[l.strip() for l in f.readlines() if l]
setup(
     name='coulomb',
     version='1.0',
     description='computing coulomb stress changes on fixed or non-uniform receiver faults',
     author='Jianjun Wang',
     author_email='jjwang@sgg.whu.edu.cn',
     packages=find_packages(),
     install_requires=INSTALL_REQUIRES,
     package_data={'coulomb':['data/*.txt']},
     url='',
     license='')
