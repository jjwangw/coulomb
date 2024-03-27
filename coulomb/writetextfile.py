import numpy as np
from . import colorstr as cls
def writetextfile(filename,data,headers):
  '''
    input:
          filename: the filename for which headerlines and data are to be save. It's a string.
	  headers: the headerlines. It's a list.
	  data: a data block with nrow times ncol
    output:
          the headers and data are save in the file. 
    dependence:
          numpy,colorstr
    usage:
         writetextfile('test.txt',['example','one'],np.array([[1,2,3],[4,5,6]]))
    version:
           v1.0 Dec.28,2023 by jjwang

  '''
  with open(filename,'w') as fp:
       for s in headers:
           fp.writelines(s+'\n')
  fp.close()
  with open(filename,'a') as fp:
      np.savetxt(fp,data,fmt='%18.10f',delimiter=' ')
  fp.close()
  print(cls.colorstr(filename+' is saved.','blue'))
if __name__=='__main__':
   filename='test.txt'
   headers=['example','one']
   data=np.array([[1,2,3],[4,5,6]])
   writetextfile(filename,data,headers)
