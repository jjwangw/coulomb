import numpy as np
import re,os
import importlib.resources as importlib_resources
from . import colorstr as cls
import pathlib
def getabspath(filename):
   '''
      input:
           filename: a filename
      output:
           the filename with absolute path if the file does exist.
      dependence:
           numpy,re,os,importlib,colorstr,pathlib
      usage:
           getpath('_sampling.txt')
      version:
           v1.0 Jan.3,2023 by jjwang

   '''
   tempfilename=filename
   pkg=importlib_resources.files("coulomb")
   filename=pkg.joinpath('data',filename)
   bfile=os.path.exists(filename)
   if bfile:
      return os.path.abspath(filename)
   else:
     bfile=os.path.exists(tempfilename)
     abspathname=os.path.abspath(tempfilename)
     if bfile:
        return abspathname
     else:
       raise Exception(cls.colorstr(abspathname+' doesn\'t exist.','red'))
#------------------------------------------------------------------------#
def getrandomfilename(filename):
   '''
     input:
          filename: a filename
     output:
          an output filename with the input filename and a random number combined.
     dependence:
          random,re
     usage:
          getrandomfilename('./test.txt')
     version:
          v1.0 Jan.4,2023 by jjwang
   '''
   randomnum=str(np.random.randint(10000,20000,size=1))
   path_name,file_name_with_extension=os.path.split(filename)
   file_name,extension=os.path.splitext(file_name_with_extension)
   output_file=file_name+randomnum+extension
   output_file=re.sub(r'[\[\]]','',output_file)
   if path_name.strip():
      output_file=path_name+'/'+output_file
   return output_file
#------------------------------------------------------------------------#
def parsefilename(filename):
   '''
     input:
          filename: a filename
     output:
          return path,file and extension for the filename
     dependence:
          os
     usage:
          path,file,ext=parsefilename('./test.txt')
     version:
          v1.0 Jan.4,2023 by jjwang
   '''
   path_name,file_name_with_extension=os.path.split(filename)
   file_name,extension=os.path.splitext(file_name_with_extension)
   return path_name,file_name,extension
if __name__=='__main__':
  print(getabspath('_stress.txt'))
  randomfilename=getrandomfilename('./test.txt')
  print('randomfilename=',randomfilename)
  path,file,ext=parsefilename('./test.txt')
  print('path=',path,'file=',file,'ext=',ext)
