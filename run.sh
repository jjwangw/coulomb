#!/usr/bin/env bash
#-----------------------------------------------#
for str in `find ./ -iname  "*.sh"`;do
    chmod +x $str
done
#-----------------------------------------------#
#check if f2py is installed
f2py_cmd=$(type f2py | cut -d" " -f1)
if [ ! "$f2py_cmd" == "f2py" ];then
     pip install f2py
fi
#clean up old files and folders created during the last installation
rm -rf build dist coulomb.egg-info
#generate the dynamic link library with f2py
cp ./coulomb/coulomb_stress.f90 .
f2py -c coulomb_stress.f90 -m coulomb_stress
mv coulomb_stress*.so ./coulomb/coulomb_stress.so
rm coulomb_stress.f90
#get the absolute directory of the dynamic library
current_dir=$(cd ./;pwd)
#setup the package
python setup.py install
#set the environment variable
bash set_environ_var.sh "$current_dir"
source ~/.bash_profile
echo "PYTHONPATH=$PYTHONPATH"
#-----------------------------------------------#
cd ./AutoCoulomb
./build_autocoulomb_lib.sh
cd ../miscell
./build_miscell_lib.sh
cd ..
#add additional scripts
python ./scripts/copy_scripts.py
