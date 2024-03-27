import numpy as np
from . import colorstr as cls
def permucolnum(x,ncols):
  '''
     input:
          x: an array with nrow times ncol.
	  ncols: a permutation for the column numbers of the array x.
     output:
          y: an array with permutated column numbers as defined in the list 'ncols' for the array x.
     dependence:
          numpy,colorstr
     usage:
          x=np.array([[1,2,3],[4,5,6]])
          print('x=',x)
          ncols=[2,1,3]
          print('ncols=',ncols)
          y=permucolnum(x,ncols)
          print('y=',y)
     version:
          v1.0 Dec.28,2023 by jjwang

  '''
  ncols=list(ncols)
  nlen_before=len(ncols)
  ncols_backup=ncols #note the order of the elements of ncols will change if np.unique(ncols) is called. So it's necessary to backup ncols.
  ncols=np.unique(ncols) #drop repeated elements
  nlen_after=len(ncols)
  if nlen_before != nlen_after:
     raise Exception(cls.colorstr('the second input parameter of \'ncols\' has repeated indices.','red'))
  nrow,ncol=x.shape
  if max(ncols)>ncol or min(ncols)<1:
     raise Exception(cls.colorstr('the elements of ncols should be in a range of one to ncol. ncol is the number of columns of the first input array \'x\'','red'))
  if len(ncols)!=ncol:
     raise Exception(cls.colorstr('the number of elements of ncols should be equal to the number of columns of the input parameter \'x\'.','red'))
  n=0
  for i in ncols_backup:
     j=i-1
     if n==0:
        temp=x[...,j].reshape(nrow,1)
     else:
        temp=np.hstack( ( temp, x[...,j].reshape(nrow,1) ) )
     n=1
  y=temp
  return y
if __name__=='__main__':
   x=np.array([[1,2,3],[4,5,6]])
   print('x=',x)
   ncols=[2,1,3]
   print('ncols=',ncols)
   y=permucolnum(x,ncols)
   print('y=',y)
