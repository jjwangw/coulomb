from . import colorstr as cls
import numpy as np
def removenan(x):
  '''
    input:
          x: an array that possibly contains nan
    output:
          y: an array after those rows of x with at least one nan are dropped.
    dependence:
          numpy,colorstr
    usage:
          reomovenan(np.array([[1,2],[np.nan,3],[4,5]]))
    version:
          v1.0 Dec.28,2023 by jjwang

  '''
  nnan=np.isnan(x).any(axis=1)
  y=np.delete(x,np.where(nnan),axis=0)
  substr='the lines with nan'
  nlinewidth=int( len(str(x[0,...]))/2 )
  halfwidth=int( (nlinewidth-len(substr))/2 )
  print(cls.colorstr('*'*halfwidth+substr+'*'*halfwidth,'blue'))
  print(x[nnan,...])
  print(cls.colorstr('*'*nlinewidth,'blue'))
#  print(cls.colorstr('*'*x.shape[1],'blue'))
  return y
if __name__=='__main__':
   x=np.array([[1,2],[np.nan,3],[4,5]])
   print('x=',x)
   y=removenan(x)
   print('y=',y)
