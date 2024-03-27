import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np
import scipy.interpolate as spi
import importlib.resources as importlib_resources
import os
import coulomb as cs
def drawCFS(lon,lat,cfs,bgeo=True,ndenser=100,cr=[-1,1],ct=False,cmap='RdBu_r',baxis=True):
   '''
      input:
           lon:the longitudes of points
	   lat:the latitudes of points
	   cfs:the coulomb stress changes at points
	   ndenser(optional):the number of sampling along the axes of x and y for gridding, interpolating and drawing.
	   bgeo(optional): if bgeo=True, then x and y axes are labeled with longitude and latitude. Otherwise, then with x and y. 
	   cr(optional): the minimum and maximum values for a colorbar. The default value is cr=[-1,1].
	   ct(optional): if ct=True, to add contours over the Coulomb stress map. if ct=Faule, then not to do so (default).
	   cmap(optional): colormap.
	   baxis(optional): if baxis=False, the y axis is reversed.
      output:
           a Coulomb stress map
      dependence:
           numpy,scipy,matplotlib,importlib,os,coulomb
      usage:
           x=np.random.normal(-1,1,100)
           y=np.random.normal(-1,1,100)
           z=np.exp(-(x*x+y*y))
           drawCFS(x,y,z,cr=[-0.5,0.5],cmap='GMT_nogreen')
           drawCFS(x,y,z,bgeo=False,cr=[-0.5,0.5],cmap='GMT_nogreen')
           drawCFS(x,y,z,bgeo=False,cr=[-0.5,0.5])
      version:
           v1.0 Dec.28,2023 by jjwang

   '''
   x=np.array(lon)
   y=np.array(lat)
   z=np.array(cfs)
   cvmin=cr[0]
   cvmax=cr[1]
   if cvmin > cvmax:
      temp=cvmin
      cvmin=cvmax
      cvmax=temp
#   print('x.shape=',x.shape,'y.shape=',y.shape,'z.shape=',z.shape)
   minx=np.min(x)
   maxx=np.max(x)
   miny=np.min(y)
   maxy=np.max(y)
   x1=np.linspace(minx,maxx,ndenser)
   y1=np.linspace(miny,maxy,ndenser)
   x2,y2=np.meshgrid(x1,y1,sparse=False)
   z2=spi.griddata((x,y),z,(x2,y2),method='cubic')
   h=plt.figure(figsize=(12,6))
   cmap=get_color(cmap)
   #cmap='RdBu_r'
   axe=plt.pcolor(x2,y2,z2,cmap=cmap,linewidths=5,vmin=cvmin,vmax=cvmax)
   if ct:
      ch=plt.contour(x2, y2, z2, [-0.1,0.1], linewidths=0.5, colors='k')
      plt.clabel(ch,[-0.1,0.1],inline=True,fontsize=18)
   ch=plt.colorbar(axe)
   ch.ax.set_ylabel('Coulomb stress changes [bars]', fontsize = 16, weight="light")
   if bgeo:
     plt.xlabel('Longitude(deg)',fontsize=16, weight="light")
     plt.ylabel('Latitude(deg)',fontsize=16, weight="light")
   else:
     plt.xlabel('X(km)',fontsize=16, weight="light")
     plt.ylabel('Y(km)',fontsize=16, weight="light")
   if not baxis:
      ax = plt.gca()
      ax.invert_yaxis()
   plt.savefig('coulomb_stress.pdf',dpi=300,edgecolor='none') 
   plt.show()
def get_color(cmap):
    pkg=importlib_resources.files("coulomb") #read a built-in colormap rather than a python-style one
    colorfile=pkg.joinpath('data',cmap)
    bcolor=os.path.isfile(colorfile)
    if bcolor:
       color_values=cs.readtextfile(colorfile,headerlines=1)       
       cmap=ListedColormap(color_values)
    return cmap
if __name__=='__main__':
   x=np.random.normal(-1,1,100)
   y=np.random.normal(-1,1,100)
   z=np.exp(-(x*x+y*y))
   drawCFS(x,y,z,cr=[-0.5,0.5],cmap='GMT_nogreen')
   drawCFS(x,y,z,bgeo=False,cr=[-0.5,0.5],cmap='GMT_nogreen')
   drawCFS(x,y,z,bgeo=False,cr=[-0.5,0.5])
