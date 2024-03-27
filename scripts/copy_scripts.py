#!/usr/bin/env python
import os,site
bin_folder=os.getcwd()+'/scripts/bin'
#print('bin_folder=',bin_folder)
#gain all scripts in the bin folder
files=os.listdir(os.getcwd()+'/scripts/bin')
#print('files=',files)
#acquire the bin directory associated with sitepackages 
package_path=site.getsitepackages()[0]
#print('package_path=',package_path)
package_path_array=package_path.split('/')[1:-3]
#print('package_path_array=',package_path_array)
bin_path=[s+'/' for s in package_path_array]
#print('bin_path=',bin_path)
total_bin_path="/"
#gain the concatenated absolute path of sitepackages
for s in bin_path:
  total_bin_path=total_bin_path+s
total_bin_path=total_bin_path+"bin"
#print('total_bin_path=',total_bin_path)
#remove and copy scripts into the bin directory
for s in files:
  bin_file=total_bin_path+'/'+s
  if os.path.isfile(bin_file):
     os.remove(bin_file) #delete the target scripts in the bin directory
#     os.system('rm '+total_bin_path+'/'+s) #delete the target scripts in the bin directory
  s=os.getcwd()+'/scripts/bin/'+s
  os.system('chmod +x '+s+';'+'cp '+s+' '+total_bin_path) #copy the scripts in the scripts directory into the bin directory 
