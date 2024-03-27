from coulomb import coulomb_stress  as cs
import numpy as np
def arrayCFS(stress,strike,dip,rake,friction,skempton):
    '''
      input:
            stress: stress tensors with nrow times 6. Each row of the stress tensors is in a format of 
	    e11 e12 e13 e22 e23 e33. The subscripts of 1, 2 and 3 correspond to the x, y and z axes.
	    The x axis is due north, y due east and z upward.
            strike: the strike angle of a receiver fault. strike is in dimension of one or nrow. 
            dip: the dip angle of the receiver fault. dip is in dimension of one or nrow.
            rake: the rake angle of the receiver fault. rake is in dimension of one or nrow.
            friction: the friction coefficient. friction is in dimension of one or nrow.
            skempton: the skempton coefficient. skempton is in dimension of one or nrow.
      output:
            shearstress: shear stresses. shearstress is in dimension of nrow.
            normalstress: normal stresses. normalstress is in dimension of nrow.
            coulombstress: coulomb stresses. coulombstress is in dimension of nrow.
      dependence:
            numpy,coulomb
      usage:
            import numpy as np
	    import coulomb as cs
	    stress=np.matrix([[1,2,3,4,5,6],[7,8,9,10,11,12]])
            strike=np.array([100,100])
            dip=np.array([30,30])
            rake=np.array([60,60])
            friction=np.array([0.5])
            skempton=np.array([0.5])
            shearstress,normalstress,coulombstress=cs.arrayCFS(stress,strike,dip,rake,friction,skempton)
      version:
            v1.0 Dec.26,2023 by jjwang

    '''
    stress=np.mat(stress)
    strike=np.array(strike)
    dip=np.array(dip)
    rake=np.array(rake)
    friction=np.array(friction)
    skempton=np.array(skempton)

    nrow=stress.shape[0]
#    print('before: friction=',friction,'skempton=',skempton)
#    print('type(stress)=',type(stress),'dimension=',stress.shape)
#    print('nrow=',nrow,'stress=',stress,'strike=',strike,'dip=',dip,'rake=',rake,'friction=',friction,'skempton=',skempton)
#
    cs.cfsmod.stress=stress
    cs.cfsmod.strike=strike
    cs.cfsmod.dip=dip
    cs.cfsmod.rake=rake
    cs.cfsmod.friction=friction
    cs.cfsmod.skempton=skempton
 #   print('cs.cfsmod.stress=',cs.cfsmod.stress,'cs.cfsmod.strike=',cs.cfsmod.strike,'cs.cfsmod.dip=',cs.cfsmod.dip)
 #   print('cs.cfsmod.rake=',cs.cfsmod.rake,'cs.cfsmod.friction=',cs.cfsmod.friction,' cs.cfsmod.skempton=', cs.cfsmod.skempton)
 #   cs.cfsmod.shearstress=np.empty(nrow,dtype=float)
 #   cs.cfsmod.normalstress=np.empty(nrow,dtype=float)
 #   cs.cfsmod.coulombstress=np.empty(nrow,dtype=float)
    cs.cfsmod.shearstress=[None]*nrow
    cs.cfsmod.normalstress=[None]*nrow
    cs.cfsmod.coulombstress=[None]*nrow
 #   print('beside cfsmode: friction=', cs.cfsmod.friction,'skempton=',cs.cfsmod.skempton)
    cs.cfsmod.arraycfs()
    return cs.cfsmod.shearstress,cs.cfsmod.normalstress,cs.cfsmod.coulombstress
if __name__=='__main__':
    stress=np.array([[2,6,4,1,5,3],[2,6,4,1,5,3]])
    strike=np.array([1,1])
    dip=np.array([2,2])
    rake=np.array([3,3])
    friction=np.array([0.4])
    skempton=np.array([0.0])
    shearstress,normalstress,coulombstress=arrayCFS(stress,strike,dip,rake,friction,skempton)
    print('shear stress:',shearstress,'\nnormal stress:',normalstress,'\ncoulomb stress:',coulombstress)
