from coulomb import coulomb_stress as cs
import importlib.resources as importlib_resources
import coulomb
import numpy as np
from . import colorstr as cls
import os
import shutil
def computeCFS(stressfile,coulombfile,strike,dip,rake,friction,skempton):
 '''
   input:
        stressfile: the filename of a stress file with a header line. Following the header line 
	is the data block. Each line of the data block is in a format of the values of e11,e12,
	e13,e22,e23 and e33. The subscripts of 1, 2 and 3 correspond to the x, y and z axes. 
	The x axis is due north, the y axis is due east and the z axis is due upward.
	
	coulombfile: the filename of Coulomb stress changes to be saved.

	strike,dip,rake: the strike, dip and rake angles of a receiver fault. They are scalars.

	friction,skempton: the friction and skempton coefficients. They are also scalars.

   output:
        The Coulomb stress changes that are saved in the file named 'coulombfile'.

   dependence:
        coulomb,importlib,numpy,colorstr,os,shutil

   usage:
       pkg=importlib_resources.files("coulomb")
       stressfile=pkg.joinpath('data','_stress.txt')
       coulombfile='test_coulomb.txt'
       strike=90.0
       dip=90.0
       rake=0.0
       friction=0.4
       skempton=0.0
       computeCFS(stressfile,coulombfile,strike,dip,rake,friction,skempton)
   version:
        v1.0 Dec.31,2023 by jjwang

 '''
 bfile=os.path.isfile(stressfile)
 if not bfile:
    raise Exception(cls.colorstr(stressfile+' doesn\'t exist.','red'))
 tempstressfile=coulomb.getrandomfilename('stress.txt')
 shutil.copy(stressfile,tempstressfile)
 tempcoulombfile=coulomb.getrandomfilename('coulomb.txt')
 cs.computecfs(tempstressfile,tempcoulombfile,strike,dip,rake,friction,skempton)
 shutil.copy(tempcoulombfile,coulombfile)
 print(cls.colorstr(coulombfile+' is created.','blue'))
 for tempfile in [tempstressfile,tempcoulombfile]:
   try:
    os.remove(tempfile)
   except OSError as error:
    print(error)
    print(cls.colorstr('failed to remove '+tempfile,'red'))
if __name__=='__main__':
  pkg=importlib_resources.files("coulomb")
  stressfile=pkg.joinpath('data','_stress.txt')
  coulombfile='test_coulomb.txt'
  strike=90.0
  dip=90.0
  rake=0.0
  friction=0.4
  skempton=0.0
  computeCFS(stressfile,coulombfile,strike,dip,rake,friction,skempton)
