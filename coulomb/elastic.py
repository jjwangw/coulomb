import numpy as np
def gradisp2strain(gradient_disp):
    '''
      input:
           gradient_disp: the gradient of a displacement vector in a 3D cartesian coordinate system.
	   It's an array with 3 times 3 like np.array([[uxx,uxy,uxz],[uyx,uyy,uyz],[uzx,uzy,uzz]]).
      output:
           a strain tensor. eij=0.5*(uij+uji).
      dependence:
           numpy
      usage:
           gradisp2strain(gradient_disp)
      version:
          v1.0 Jan.8,2023 by jjwang
 
    '''
    gradient_disp=np.array(gradient_disp)
    if gradient_disp.shape != (3,3):
      raise Exception('the gradient of a displacement vector should be in three times three dimensions.')
    strain=np.zeros((3,3))
    for i in range(3):
      for j in range(3):
        strain[i,j]=0.5*(gradient_disp[i,j]+gradient_disp[j,i])
    return strain
def strain2stress(strain,lambdap,mu):
    '''
      input:
           strain: a strain tensor with 3 times 3.
	   lambdap: a Lamé parameter.
	   mu: shear modulus, the second Lamé parameter.
      output:
           a stress tensor.
      dependence:
           numpy
      usage:
           strain2stress(strain,lambdap,mu)
      version:
           v1.0 Jan.8,2023 by jjwang 
    '''
    strain=np.array(strain)
    if strain.shape != (3,3):
      raise Exception('the strain tensor should be in three times three dimensions.')
    stress=np.zeros((3,3))
    dilation=(strain[0,0]+strain[1,1]+strain[2,2])
    for i in range(3):
       for j in range(3):
           if i==j:
               deltaij=1.0
           else:
               deltaij=0.0
           if i>j:
               stress[i,j]=stress[j,i]
           else:
               stress[i,j]=lambdap*dilation*deltaij+2*mu*strain[i,j]
    return stress
def trans_displacement(disp,strike):
    '''
      input:
           disp: the displacement vector at an observational point due to earthquake faulting of a source fault
	   in a fault coordinate system whose x axis is due strike, z axis is upward and y axis is the cross product 
	   of the z and x axes.
	   The input argument 'disp' can be in a dimension of nrows times 3. The first column is related to x,
	   the second y and the third z.
	   strike: the strike angle of the source fault. It's a scalar and has a unit of degree.
      output:
           the transformed displacement vector in a local Cartesian coordinate system whose x axis is due north,
	   y due east and z upward.
      dependence:
           numpy
      usage:
      version:
           v1.0 Jan.8,2023 by jjwang
 
    '''
    disp=np.array(disp)
    if disp.shape[1] !=3:
      raise Exception('the displacment matrix should be in nrow times 3 dimensions.') 
    phi=np.pi/180.0*strike
    cosphi=np.cos(phi)
    sinphi=np.sin(phi)
    D=np.array([[cosphi,sinphi,0],
               [sinphi,-cosphi,0],
	       [0,0,1]])
    DT=D.T
    newdisp=np.dot(disp,DT)
    return newdisp
def trans_stresstensor(stress,strike):
    '''
      input:
           stress: a stress tensor in a fault coordinate system whose x axis is due strike, z axis is upward and y axis 
	   is the cross product between the z and x axes. It's an array with 3 times 3.
      output:
           a rotated stress in a local Cartesian coordinate system whose x axis is due north, y due east and z upward.
      dependence:
           numpy
      usage:
           trans_stresstensor(stress,strike)
      version:
            v1.0 Jan.8,2023 by jjwang
 
    '''
    stress=np.array(stress)
    if stress.shape != (3,3):
      raise Exception('the stress tensor should be in three times three dimensions.')
    phi=np.pi/180.0*strike
    cosphi=np.cos(phi)
    sinphi=np.sin(phi)
    D=np.array([[cosphi,sinphi,0],
               [sinphi,-cosphi,0],
	       [0,0,1]])
    DT=D.T;
    temp=np.dot(D,stress)
    newstress=np.dot(temp,DT)
    return newstress
def flatten_stress(stress):
    '''
      input:
          a stress tensor that is in a dimension of 3 times 3.
      output:
          an array of the six independent components of the stress tensor, which is like np.array([exx exy exz eyy eyz ezz])
      dependence:
          numpy
      usage:
          flatten_stress(stress)
      version:
           v1.0 Jan.8,2023 by jjwang
 
    '''
    
    stress=np.array(stress)
    if stress.shape != (3,3):
      raise Exception('the stress tensor should be in three times three dimensions.')
    flat_stress=np.array([[stress[0,0],stress[0,1],stress[0,2],stress[1,1],stress[1,2],stress[2,2]]])
    return flat_stress
