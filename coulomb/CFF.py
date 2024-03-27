from coulomb import coulomb_stress as cs
import numpy as np
from . import colorstr as cls
def CFF(stress,strike,dip,rake,friction,skempton):
 '''
    input:
         stress: an array with one times six in a format of e11 e12 e13 e22 e23 e33.
	 The subscripts of 1, 2 and 3 correspond to the x, y and z axes, respectively.
	 The x axes is due north, y due east and z upward.
	 strike,dip,rake: the strike, dip and rake angles of a fixed receiver fault, which are
	 scalars.
	 friction,skempton: the friction and skempton coefficent, which are scalars.
    output:
         shearstress,normalstress,coulombstress
    dependence:
         numpy,coulomb_stress,colorstr
    usage:
         x=np.array([2,6,4,1,5,3])
         shearstress,normalstress,coulombstress=CFF(x,1.0,2.0,3,0.4,0.0)
         print('shearstress=',shearstress,'normalstress=',normalstress,'coulombstress=',coulombstress)
    version:
         v1.0 Dec.31,2023 by jjwang

 '''
 stress=np.array(stress)
 stress=stress.flatten()
 if len(stress)!=6:
    raise Exception(cls.colorstr('the input parameter of stress should be an array with 6 elements.','red'))
 shearstress,normalstress,coulombstress=cs.cff(stress,strike,dip,rake,friction,skempton)
 return shearstress,normalstress,coulombstress
if __name__=='__main__':
  x=np.array([2,6,4,1,5,3])
  shearstress,normalstress,coulombstress=CFF(x,1.0,2.0,3,0.4,0.0)
  print('shearstress=',shearstress,'normalstress=',normalstress,'coulombstress=',coulombstress)
