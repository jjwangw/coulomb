import coulomb as cs
from . import colorstr as cls
import numpy as np
import os
#def onestepCFS(stressfile,samplingfile,strike,dip,rake,friction,skempton,
#               coulombfile='coulomb.txt',bdraw=True,bgeo=True,cr=[-0.5,0.5],ct=False,ndenser=300,cmap='RdBu_r',**kwargs):
def onestepCFS(stressfile,samplingfile,
               coulombfile='coulomb.txt',bdraw=True,bgeo=True,cr=[-0.5,0.5],ct=False,ndenser=300,cmap='RdBu_r',**kwargs):
 '''
    input:
         stressfile: the filename of a stress file with a headerline of 'e11 e12 e13 e22 e23 e33'.
	 The subscripts of 1, 2 and 3 stand for x, y and z axes, respectively. Each line of the subsequent 
	 data block after the header line is the six components of a stress tensor resulting from 
	 a volcano or an earthquake. The stress tensor is tied to a local coordinate system whose x is due north, 
	 y is due east and z is upward. The bar is the unit of each components of the stress tensor.

	 samplingfile: 
	 case 1: the filename of a sampling file with a header line of 'lat.(deg) lon.(deg) depth(km)' or
	 'lat(deg) lon(deg) depth(km) strike(deg) dip(deg) rake(deg) friction skempton'. Following the headerline 
	 are corresponding values at each line. The coordinates from this file is related to a geodetic coordinate system.
	 case 2: the filename of the sampling file with a headerline of 'x(km) y(km) depth(km)' or
	 'x(km) y(km) depth(km) strike(deg) dip(deg) rake(deg) friction skempton'. Following the headerline
	 are corresponding values at each line. The coordinates from this file is related to a Cartesian coordinate system
	 whose x is due north, y is due east and z is upward.
	 
	 coulombfile: the filename of the resulting Coulomb stress changes. Its default filename is coulomb.txt.

	 bdraw: if bdraw=True (default), then to draw Coulomb stress changes. if bdraw=False, then not to do so.

	 bgeo: if bgeo=True(default), then a geodetic coordinate system is accounted for. Otherwise, a Cartesian coordinate system.

	 cr: the color range of a colorbar when displaying the Coulomb stress changes. Its default value is [-0.5,0.5]. 
	 
	 ct: if ct=False(default), then not to draw contours. If ct=True, then to do so.

	 ndenser: the number of gridding along x and y axes when displaying the Coulomb stress changes. The larger this
	 value is, the smoother the Coulomb stress changes are. Its default value is 300.

         cmap: the color map for drawing Coulomb stress changes. The default color map is the build-in map of 'RdBu_r'.

	 **kwargs: they are strike,dip,rake,friction,skempton. The strike, dip and rake angles of a receiver fault can be scalar or
	 row vectors with n rows. n is also the total line numbers of the stress file excluding the headerline. the friction and 
	 skemtpon coefficients are often set to 0.4 and 0, respectively. These two coefficient can be scalar or row vectors with
	 n rows. n has the same meaning as aformentioned.
    ooutput:
         the Coulomb stress changes are saved in the 'coulombfile' file.
    dependence:
         coulomb,numpy,os
    usage:
         stressfile='test_stress.txt'
         samplingfile='test_sampling.txt'
         x=np.array(range(1,7)).reshape(1,6)
         np.savetxt(stressfile,x,fmt='%13.6f',delimiter=' ',header='e11 e12 e13 e22 e23 e33',comments='')
         sampling=np.array([1,1,1]).reshape(1,3)
         np.savetxt(samplingfile,sampling,fmt='%13.6f',delimiter=' ',header='lat.(deg),lon.(deg) depth(km)',comments='')
         strike=90.0
         dip=60.0
         rake=30.0
         friction=0.4
         skempton=0.0
         onestepCFS(stressfile,samplingfile,coulombfile='test_coulomb.txt',bdraw=False,
		   strike=strike,dip=dip,rake=rake,friction=friction,skempton=skempton)
    version:
         v1.0 on Dec.30,2023 by jjwang
	 on Jan.5,2024: add **kwargs 
 '''
 stress=cs.readtextfile(stressfile,headerlines=1)
 samplingpoints=cs.readtextfile(samplingfile,headerlines=1)
 strike=None
 dip=None
 rake=None
 friction=None
 skempton=None
 for key,value in kwargs.items():
    lowerkey=key.lower()
    value=scalar2array(value) #note the array type ensures a correct passing for arguments to a fortran module.
#    print('key=',key,'value=',value)
    if lowerkey=='strike':
        strike=value
    if lowerkey=='dip':
        dip=value
    if lowerkey=='rake':
        rake=value
    if lowerkey=='friction':
        friction=value
    if lowerkey=='skempton':
        skempton=value
 if samplingpoints.shape[1]==3:
    if (strike==None).any():
      raise Exception(cls.colorstr('the argument ''strike'' is not set.','red'))
    if (dip==None).any():
      raise Exception(cls.colorstr('the argument ''dip'' is not set.','red'))
    if (rake==None).any():
      raise Exception(cls.colorstr('the argument ''rake'' is not set.','red'))
    if (friction==None).any():
      raise Exception(cls.colorstr('the argument ''friction'' is not set.','red'))
    if (skempton==None).any():
      raise Exception(cls.colorstr('the argument ''skempton'' is not set.','red'))
 elif samplingpoints.shape[1]==8:
    strike=samplingpoints[...,3]
    dip=samplingpoints[...,4]
    rake=samplingpoints[...,5]
    friction=samplingpoints[...,6]
    skempton=samplingpoints[...,7]
 else:
    raise Exception(cls.colorstr('the format of the sampling file is incorrect. It''s data block should have 3 or 8 columns.','red'))
# print('stress=',stress,'strike=',strike,'dip=',dip,'rake=',rake,'friction=',friction,'skempton=',skempton)
 shearstress,normalstress,coulombstress=cs.arrayCFS(stress,strike,dip,rake,friction,skempton)
# print('shearstress=',shearstress,'normalstress=',normalstress,'coulombstress=',coulombstress)
 samplingcoulomb=np.stack((samplingpoints[...,1],samplingpoints[...,0],samplingpoints[...,2],
                           shearstress,normalstress,coulombstress),axis=1)
 headers=['         lon.(deg)          lat.(deg)          depth(km)       shearstress(bar)   normalstress(bar)  coulombstress(bar)']
 cs.writetextfile(coulombfile,samplingcoulomb,headers)
 if bdraw:
    newdata=cs.removenan(samplingcoulomb) #it's crucial to remove those lines with nan, ensuring interpolating before drawing figure successfully.
    cs.drawCFS(newdata.T[0],newdata.T[1],newdata.T[5],bgeo=bgeo,cr=cr,ct=ct,ndenser=ndenser,cmap=cmap)
 #print(cls.colorstr(coulombfile+' is created.','blue'))
def scalar2array(x):
    y=[x]
    y=np.array(y)
    y=y.flatten()
    return y
if __name__=='__main__':
   stressfile='test_stress.txt'
   samplingfile='test_sampling.txt'
   x=np.array([2,6,4,1,5,3]).reshape(1,6)
   np.savetxt(stressfile,x,fmt='%13.6f',delimiter=' ',header='e11 e12 e13 e22 e23 e33',comments='')
   sampling=np.array([1,1,1]).reshape(1,3)
   np.savetxt(samplingfile,sampling,fmt='%13.6f',delimiter=' ',header='lat.(deg),lon.(deg) depth(km)',
              comments='')
   strike=1
   dip=2
   rake=3
   friction=0.4
   skempton=0.0
   onestepCFS(stressfile,samplingfile,coulombfile='test_coulomb.txt',bdraw=False,
              strike=strike,dip=dip,rake=rake,friction=friction,skempton=skempton)
