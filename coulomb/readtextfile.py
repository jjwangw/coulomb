import numpy as np
import os
import importlib.resources as importlib_resources
from . import colorstr as cls
def readtextfile(filename,headerlines=0,bpackage=0):
 '''
   input:
        filename: the filename of a text file.
  	headerlines: the number of the header lines to be skipped for the file.
	bpackage: if bpackage=1, then read a text file from the 'coulomb' package where 
	          the file is saved in the subfolder of data.
                  if bpackage=0 (default), then read a text file from any directory assgined
		  rather than from the data subfolder of the 'coulomb' package.
   output:
         data: it is the data block of the text file. For the 'coulomb' package, three kinds of files are accounted for.
	      case 1:
	            stress file: the data block of the text file with nrow times six in a type of np.array. Each line
                    includes the six components of the stress tensor at a grid point with an arrangement
	            of e11, e12, e13, e22, e23 and e33 in a local coordinate system whose x is due north,
	            y is due east and z is upward.
	      case 2:
		    sampling file: the data block of the text file with nrow times three. Each line has the format of
		    'latitude(deg) longitdue(deg) depth(km)'.
		    Or the data block of the text file with nrow times eight. Each line has the format of 
		    'latitude(deg) longitude(deg) depth(km) strike(deg) dip(deg) rake(deg) friction skempton'.
	      case 3:
	            slip model: the data block of the text file with nrow times fourteen. Each line is in a format of
		    'latitude(deg) longitude(deg) depth(km) length(km) width(km) AL1(km) AL2(km) AW1(km) AW2(km) strike(deg) dip(deg) strike_slip(m) dip_slip(m) tensile_slip(m)'.
	            
   usage:
        data=readtextfile('stress.txt',headerlines=1,bpackage=1)
   dependence:
        numpy,os,importlib,colorstr
   version:
        v1.0: Dec.27,2023 by jjwang

 '''
 if bpackage==1:
    pkg=importlib_resources.files("coulomb")
    filename=pkg.joinpath('data',filename)
 bfile=os.path.exists(filename)
 if not bfile:
    print('filename=',filename)
    raise Exception(cls.colorstr(str(filename)+' doesn\'t exist.','red'))
 data=[]
 with open(filename,'r') as fp:
    ncount=0
    lines=fp.readlines()
    for line in lines:
      temp=line.strip('\n').split()
      if ncount>=headerlines:
         line=[float(x) for x in temp]
         data.append(line)
      ncount=ncount+1
 data=np.array(data)
 return data
 #
if __name__=='__main__':
    #data=readtextfile('no_exist_file',headerlines=0,bpackage=1)
    data=readtextfile('_stress.txt',headerlines=1,bpackage=1)
    print('data=',data)
