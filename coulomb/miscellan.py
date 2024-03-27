from coulomb import samplingpointsgivendepth as sp
import coulomb as cs
import numpy as np
import shutil,os
from . import colorstr as cls
#import colorstr as cls
from coulomb import preprocsampling_profile as pf
import matplotlib.pyplot as plt
import re
import scipy.interpolate as spi
def gridcfs(lon,lat,cfs,ndenser=100):
  '''
    input:
         lon: a column vector
	 lat: another column vector
	 cfs: a third column
	 ndenser: a number for densifying grids
    output:
         densified grids and their values
    dependence:
         numpy,scipy
    usage:
    version:
       v1.0 on Jan.4,2024 by jjwang
  '''
  x=np.array(lon)
  y=np.array(lat)
  z=np.array(cfs)
  minx=np.min(x)
  maxx=np.max(x)
  miny=np.min(y)
  maxy=np.max(y)
  x1=np.linspace(minx,maxx,ndenser)
  y1=np.linspace(miny,maxy,ndenser)
  x2,y2=np.meshgrid(x1,y1,sparse=False)
  z2=spi.griddata((x,y),z,(x2,y2),method='cubic')
  return x2,y2,z2
def draw_profile(profile,**kwargs):
 '''
   input:
        profile: the filename of a gridded profile.
	**kwargs: variable-length arguments, which are figsize='8/6' and aftershock=aftershockname.
	         aftershockname is the filename of aftershocks with a format of lon. lat. and depth.
   output:
        the split files with gridded profile and mapped aftershocks.
   dependence:
        matplotlib,numpy,re,os
   usage:
   version:
        v1.0 on Jan.4,2024 by jjwang
 '''
 aftershock=None
 figsize='8/6'
 for key,value in kwargs.items():
      #print('key=',key,'value=',value)
      if key=='aftershock':
         aftershock=value
      elif key=='figsize':
         figsize=value
      else:
        raise Exception(cls.colorstr('wrong keyword arguments.','red'))
 A=np.loadtxt(profile, skiprows=2,dtype=float)
 string=re.sub(' ','',figsize)
 width,height=re.split('/',string)
 size=(float(width),float(height))
 plt.rcParams['figure.figsize']=size
 plt.rcParams.update({'font.size': 18})
 plt.figure()
 ax = plt.axes(projection='3d')
 ax.scatter(A[...,1],A[...,0],A[...,2],s=10,color='red',label='grid points')
 ax.set_zlabel('Depth [km]')
 minlon=min(A[...,1])
 maxlon=max(A[...,1])
 minlat=min(A[...,0])
 maxlat=max(A[...,0])
 minz=min(A[...,2])
 maxz=max(A[...,2])
 offset=0.05
 epsilon=5.0e-1
 if np.abs(minlon-maxlon)<=epsilon:
    minlon=minlon*(1-offset)
    maxlon=maxlon*(1+offset)
 if np.abs(minlat-maxlat)<=epsilon:
    minlat=minlat*(1-offset)
    maxlat=maxlat*(1+offset)
 #print([minlon,maxlon,minlat,maxlat,minz,maxz])
 #plt.axis((minlon,maxlon,minlat,maxlat))
 plt.axis([minlon,maxlon,minlat,maxlat,minz,maxz])
 #ax.set_zlim(minz,maxz)
 plt.title('A profile in 3D')
#
 if aftershock != None:
    B=np.loadtxt(aftershock, skiprows=1,dtype=float)
    ax.scatter(B[...,1],B[...,0],B[...,2],color='blue',label='mapped aftershocks')
    plt.legend(loc='best')
 ax.xaxis.set_major_formatter('{x:.1f}$^\circ$')
 ax.yaxis.set_major_formatter('{x:.1f}$^\circ$')
 ax.invert_zaxis()
 plt.show()
#
 plt.figure()
 plt.plot(A[...,3],A[...,4],'r.',label='grid points')
 if aftershock !=None:
   plt.plot(B[...,3],B[...,4],'b.',label='mapped aftershocks')
 ax = plt.gca()
 ax.invert_yaxis()
 ax.set_xlabel('Along strike [km]')
 ax.set_ylabel('Along Downdip [km]')
 plt.title('A profile in 2D')
 plt.legend(loc='best')
 plt.show()
def sampling_points_given_depth(hrange,vrange,depth=10,outputfile='samplingpoints.txt'):
 '''
   input:
        hrange: the grid range along the horizontal axis. hrange=[minvalueh,maxvalueh,dvalueh].
	minvalueh and maxvalueh are the minimum and maximum values for the grid range. dvalueh is 
	the step of gridding points.

	vrange: the grid range along the vertical axis. vrange=[minvaluev,maxvaluev,dvaluev].
	minvaluev and maxvaluev are the minimum and maximum values for the grid range. dvaluev is 
	the step of gridding points.

	depth: the depth of a horizontal plane on which sampling points are located. It's a scalar in km.
	It's default value is 10.

	outputfile: the filename of an output file, in which sampling points are saved. The first line of the output file
	is the total number of sampling points. Then the following lines are in a format of lat. lon. depth or x y depth.
	lat, lon. and depth are the latitude, longitude and depth for each grid point in a geodetic coordinate system, 
	while x y and depth are the northern, eastern and downward components of the coordinate at each grid point in a local 
	cartesian coordinate system.

   output:
        the sampling points are saved in the file named outputfile.
   dependence:
        samplingpointsgivendepth,coulomb,numpy,shutil,os,colorstr
   usage:
        sampling_points_given_depth([100,102,0.05],[30,34,0.05],depth=8,outputfile='test_sampling.txt')
   version:
       v1.0 on Jan.4,2024 by jjwang
 '''
 hrange=np.array(hrange)
 vrange=np.array(vrange)
# print('hrange=',hrange,'vrange=',vrange)
 minlon=hrange[0]
 maxlon=hrange[1]
 dlon=hrange[2]
 minlat=vrange[0]
 maxlat=vrange[1]
 dlat=vrange[2]
 depth=np.array(depth)
 output_file=cs.getrandomfilename(outputfile)
 sp.samplingpointsgivendepth(minlon,maxlon,dlon,minlat,maxlat,dlat,depth,output_file)  
 shutil.copy(output_file,outputfile)
 os.remove(output_file)
 prompt_info=cs.getabspath(outputfile) + ' is created.'
 print(cls.colorstr(prompt_info,'blue'))
 #preprocsampling_profile(profilename,nL,nW,extendLW,aftershockfilename,samplingprofilename)
def samplingprofile(profilename,nL=50,nW=50,extendLW=[0,1,0,1],aftershockfilename="",
                    samplingprofilename="sampling.txt",bdraw=True,figsize='8/6'):
 '''
   input:
        profilename: the input filename of rectangular profiles. Its format is as follows. The first line is the total
	number of profiles. Then each of the following line is in a format of 'lat lon depth length width AL1 AL2 AW1
	AW2 strike dip'. lat,lon and depth are related to the reference point of the rectangular profile for the given
	line in the input file. length and width are the long and short edges of the rectangular profile, respectively. 
	AL1 is not positive and its asbolute value |AL1| is the distance of the reference point to the left edge of the 
	rectangular profile. AL2 is not negative and it is the distance of the reference point to the right edge of the 
	rectangular profile. AW1 is not positive and its absolute value |AW1| is the distance of the reference point to 
	the lower edge of the rectangular profile. AW2 is not negative and it is the distance of the reference point to 
	the upper edge of the rectangular profile. strike and dip are the strike and dip angles of the profile, respectively. 

	nL: the sampling number along strike. Its default value is 50.

	nW: the sampling number along updip. Its default value is 50.

	extendLW: it's a row vector with four elements as [k1,k2,k3,k4], which are the scalar factors for extending the
	rectangular profile with respect to the lower left corner of the profile. The original lower left corner is at (0,0). 
	If the profile is extended, the new lower left corner is at (k1*L,k3*W). This coordinate is referred to the fault plane
	coordinate system whose x axis is due strike, y due updip and z along normal. The default values are as follows: k1=0,k2=1,
	k3=0,k4=1.

	aftershockfilename: the filename of aftershocks in a format of longitude, latitude and depth with a headerline. These
	aftershocks are to be projected onto the rectangular profile. Its default value is empty, which means not to map aftershocks.

	samplingprofilename: the filename of a sampling profile. In this file there has at least one data block pertaining to
	the sampling points on the profile. If the argument of aftershockfilename is set, then the additional data block following the
	prior data block is associated with the projected aftershocks.
	
	bdraw: bdraw=True(default) for displaying gridded profile. bdraw=False for not doing so.
	
	figsize: set the figure size to be drawn if bdraw=True. The default value is 5/4.

   output:
        output files with sampling points on the profiles and sometimes projected aftershocks.
   dependence:
        coulomb,shutil,colorstr,os,colorstr 
   usage:
   version:
        v1.0 on Jan.4,2024 by jjwang
 '''
 extendLW=np.array(extendLW)
 profile_name=cs.getrandomfilename(profilename)
 shutil.copy(profilename,profile_name)
 pathname,filename,extension=cs.parsefilename(samplingprofilename)
 samplingprofile_name=filename+extension
 aftershockfile_name=aftershockfilename
 if aftershockfilename.strip():
   aftershockfile_name=cs.getrandomfilename(aftershockfilename)
   shutil.copy(aftershockfilename,aftershockfile_name)
 pf.preprocsampling_profile(profile_name,nL,nW,extendLW,aftershockfile_name,samplingprofile_name)
 os.remove(profile_name)
 if aftershockfilename.strip():
   os.remove(aftershockfile_name)
 with open(profilename,'r') as f:
   nline=f.readline()
 f.close()
 for i in np.arange(int(nline)):
   i=i+1
   tempfilename=filename+str(i)+extension
   if not pathname:
     outputfilname='./'+tempfilename
   else:
     outputfilname=pathname+'/'+tempfilename
     if pathname != '.': #in case that pathname='.'
        shutil.copy(tempfilename,outputfilname)
        os.remove(tempfilename)
   prompt_info=cs.getabspath(outputfilname) + ' is created.'
   print(cls.colorstr(prompt_info,'blue'))
   if bdraw:
     pathname,filename,extension=cs.parsefilename(outputfilname)
     split_profile=pathname+'/'+filename+'_profile'+extension
     split_aftershock=pathname+'/'+filename+'_aftershocks'+extension
     split_grids=pathname+'/'+filename+'_profile_grids'+extension
     for s in [split_profile,split_aftershock,split_grids]:
      if os.path.isfile(s):
         os.remove(s) #remove prior files beforehand
     os.system('split_sampling_profile.sh '+outputfilname)
     #print('split_aftershock=',split_aftershock)
     if not os.path.isfile(split_aftershock):
        split_aftershock=None
     #os.system('draw_profile.py -p '+split_profile+' -s '+figsize)
     #draw_profile(split_profile,figsize=figsize)
     print('split_profile=',split_profile,'aftershock=',split_aftershock)
     draw_profile(split_profile,aftershock=split_aftershock,figsize=figsize)
if __name__=='__main__':
 sampling_points_given_depth([100,102,0.05],[30,34,0.05],depth=8,outputfile='test_sampling.txt')
 file_profile=cs.getabspath('_profile.txt')
 file_aftershock=cs.getabspath('_aftershocks.txt')
 samplingprofile(file_profile,figsize='12/9')
