from coulomb import autocoulomb as aclb
import coulomb as cs
import os,shutil
import re
#from . import colorstr as cls
from coulomb import colorstr as cls
def AutoCoulomb(slipmodel,samplingfile,meridian=999,stressfile='stress.txt',coulombfile='coulomb.txt',
                strike=90,dip=90,rake=0,friction=0.4,skempton=0.0,bgeo=True,ndenser=100,bdraw=True,cr=[-1,1],ct=False,cmap='RdBu_r'):
   '''
      input:
           slipmodel: the slip model of a source fault. The first line of this file is the total number
           of subpatches. The following second line is as follows: 
           case 1(bgeo=True):
	   lat. lon. depth L W AL1 AL2 AW1 AW2 strike dip s1 s2 s3. The subsequent lines are similar to the second line. 
	   L and W are the length and width of a fault plane or subpatch. |AL1| and AL2 are distances of a reference point
	   on the fault or subpatch to the left edge and right edge, respective. AL1 is always non-positive, and AL2 is always
           non-negative. Likewise, |AW1| and AW2 are distances of the reference point on the fault or subpatch to
           the downdip edge and updip edge, respectively. AW1 is always non-positive and AW2 is always non-negative.
           There are relations: L=|AL1|+AL2 and W=|AW1|+AW2. The values of AL1,AL2,AW1 and AW2 allow a unique location
           of the reference point, with the combination of its depth with respect to the Earth''s surface. The units of
           lat., lon.,strike and dip are in degrees. The units of depth,L,W,AL1,AL2,AW1,AW2 are in kilometers,
           and those of s1,s2,s3 are in meters. s1,s2,s3 are components of strike-slip, dip-slip and tensile dislocations,
	   respectively.
	   case 2(bgeo=False):
	   x y depth L W AL1 AL2 AW1 AW2 strike dip s1 s2 s3. These variables have the same meanings as those in case 1 except for
	   the first two ones. x and y are the northern and eastern components of coordinates in this case, respectively.  

	   samplingfile: the sampling points at which Coulomb stress changes are resovled. This file has two formats.
           The common first line is the total number of sampled grid points. Yet the following lines differ.
	   case 1(bgeo=True)
           The subsequent lines are in a format of lat.(deg) lon.(deg) depth(km). In this subcase, the strike, dip and rake angles
	   of receiver faults should be assigned. Their default values are 90, 90 and 0. Or the subsequent lines are in a format 
	   of lat.(deg) lon.(deg). depth(km) strike(deg) dip(deg) rake(deg) friction skempton. In the latter subcase, it's not 
	   necessary to assign the strike, dip and rake angles because such values are to be read from the sampling file.

	   case 2(bgeo=False)
           The subsequent lines are in a format of x(km) y(km) depth(km) or x(km) y(km). Their default values are 90, 90 and 0.
	   Or x(km) y(km) depth(km) strike(deg) dip(deg) rake(deg) friction skempton. x and y are the northern and eastern 
	   components of coordinates. In the latter subcase, it's not necessary to assign the strike, dip and rake angles because
	   such values are to be read from the sampling file.

	   meridian: the merdian for the gaussian projection in degrees. It can be the average longitude of a target region.
	   This parameter works for bgeo=True. In the case of bgeo=False, this parameter doesn't affect coordinates related to the source
	   faults and receiver faults because those coordinates are tied to a cartesian coordinate system rather than a gedetic 
	   coordinate system. In the latter case, let its value be the default one.

	   stressfile:  stress tensors at grid points. The first line of this file is e11 e12 e13 e22 e23 e33, a header line. 
	   These components belong to a coordinate system of which axes of x, y and z are due north, due east and upward,
	   respectively. The subsequent lines are their values with units of bars.
	   
	   coulombfile: the file where Coulomb stress changes are saved. The first line is a header line with a string of 
	   lon. lat. shear_stress(bar) normal_stress(bar) coulomb_stress(bar). The subsequent lines are their values.

	   strike: the strike angle of the receiver fault. It's in [0,360] with unit being degrees. It's default value is 90.

	   dip: the dip angle of the receiver fault. It's in [0,90] with unit being degrees. It's default value is 90.

	   rake: the rake angle of the receiver fault. It's in [0,360] or [-180,180] with unit being degrees. It's default value
	   is 0.

	   friction: the friction coefficient of the receiver fault.It is in a range of 0 to 1. It's default value is 0.4.

	   skempton: the skempton's coefficient. It ranges from 0 to 1. It's default value is 0.0.

	   bgeo: bgeo=True (default) for the case when coordinates related to the slip-model file  and sampling file are in a geodetic
	   coordinate system. bgeo=False for the case when coordinates related to the files are in a cartesian coordinate system.
	   
	   ndenser: ndenser=100(default) for densifying the grids at which Coulomb stress changes are to be interpolated. This
	   parameter controls the smoothness of a Coulomb stress map.
	   
	   bdraw: bdraw=True(default) for drawing a Coulomb stress map. bdraw=False for not doing so.

           cr: the color range. cr=[-1,1](default). It means the values of the color range are set to be from -1 bar to 1 bar.
	   
	   ct: ct=False for not displaying contours of the Coulomb stress map. ct=True for doing so.

	   cmap: the colormap. ct='RdBu_r'(default). Other colormaps like ct='ANATOLIA', ct='GMT_nogreen', ct='no_green32', ct='no_green64',
	   ct='no_green128' and ct='no_green256' are also okay.
      output:
          the stress file named as stressfile
	  the Coulomb-stress-change file named as coulombfile
      dependece:
          coulomb,os,shutil,re,numpy,colorstr
      usage:
         AutoCoulomb('_slipmodel.txt','_sampling.txt',meridian=102,ndenser=300,cr=[-5,5],ct=False,cmap='RdBu_r')
         AutoCoulomb('_slipmodelxy.txt','_samplingxy.txt',bgeo=False,ndenser=300,cr=[-5,5],ct=False,cmap='RdBu_r')
      version:
          v1.0 Jan.1,2024 by jjwang
   '''
   if bgeo:
     if meridian==999:
        raise Exception(cls.colorstr('a meridian within a range of 0 to 360 should be set for the gaussian projection, e.g. consider the average longitude of the target topographical region.','red'))
     bbgeo=1
   else:
     bbgeo=0
   slip_model_file=cs.getrandomfilename('slipmodel_.txt')
   sampling_points_file=cs.getrandomfilename('samplingpoints_.txt')
   #get the absolute path
   slipmodel_path=cs.getabspath(slipmodel)
   samplingfile_path=cs.getabspath(samplingfile)
   #
   shutil.copyfile(slipmodel_path,slip_model_file)
   shutil.copyfile(samplingfile_path,sampling_points_file)
   coulomb_file=coulombfile
   stress_file=stressfile
   aclb.autocoulomb(slip_model_file,sampling_points_file,coulomb_file,stress_file,meridian,strike,dip,rake,friction,skempton,bbgeo)
   data=cs.readtextfile(coulomb_file,headerlines=1)
   if bdraw:
      cs.drawCFS(data[...,0],data[...,1],data[...,4],bgeo=bgeo,ndenser=ndenser,cr=cr,ct=ct,cmap=cmap)
   os.remove(slip_model_file)
   os.remove(sampling_points_file)
if __name__=='__main__':
   AutoCoulomb('_slipmodel.txt','_sampling.txt',meridian=102,ndenser=300,cr=[-5,5],ct=False,cmap='ANATOLIA')
   AutoCoulomb('_slipmodelxy.txt','_samplingxy.txt',bgeo=False,ndenser=300,cr=[-5,5],ct=False,cmap='ANATOLIA')
   AutoCoulomb('_slipmodelxy.txt','_samplingxy.txt',bgeo=Fase,ndenser=300,cr=[-5,5],ct=False,cmap='RdBu_r')
