#!/usr/bin/env bash
#coded on Dec.25,2023 by jjwang
current_dir=$1
#
if [ $# -ne 1 ];then
  echo -e "\033[31m Usage: set_environ_var.sh <pathname>\033[0m. The parameter of 'pathname' in a command line is a relative or absolute directory containing dynamic libraries (*.so). If to set other environment variables, please modify the names of COULOMBLIB and PYTHONPATH to be other ones."
  exit 1
fi
#
environ_var=COULOMBLIB
environ_file=~/.bash_profile
directory_environ=$(dirname $environ_file)
basefile_environ=$(basename $environ_file)
environ_file_backup="$directory_environ/""${basefile_environ%%.*}"_backup
if [ ! -f "$environ_file" ];then
   touch "$environ_file"
fi
#backup the .bash_file for emergency recovery in case of the environment variable file being crashed. 
if [ ! -f "$environ_file_backup" ] || [ ! -s "$environ_file_backup" ];then
  cp $environ_file $environ_file_backup
fi
N=$(grep COULOMBLIB "$environ_file" | wc -l | awk '{print $1}')
nlines=$(cat $environ_file | wc -l | cut -d":" -f1 )
osname=$(uname)
if [ $osname == 'Darwin' ];then #make the sed command be adaptable to a different OS. 
   sedi=".bk"
fi
if [ "$N" -eq 0  ];then #if the environment variable named COULOMBLIB doesn't exist, then append it to the end of the .bash_file
   if [ "$nlines" -gt 0 ];then #if the environment variable file exists and it's not empty, then append the environment variable
   sed -i "$sedi"  "${nlines}a \\
COULOMBLIB=$current_dir \\
export PYTHONPATH=\"\$COULOMBLIB\":\"\$PYTHONPATH\"
" "$environ_file"
   else #if the environment variable file doesn't exist or is empty, redirect it.
      echo "environ_file=$environ_file"
      echo "COULOMBLIB=$current_dir" >  "$environ_file"
      echo 'export PYTHONPATH="$COULOMBLIB":"$PYTHONPATH"' >> "$environ_file"
   fi
else  #if the environment variable exists, then update it. Note that the name of the environment should not conflict with other ones.
   sed -i "$sedi" "s|.*COULOMBLIB.*=.*|COULOMBLIB=$current_dir|g" "$environ_file"
   sed -i "$sedi" "s|.*export.*COULOMBLIB.*|export PYTHONPATH=\"\$COULOMBLIB\":\"\$PYTHONPATH\"|g" "$environ_file"
fi
echo -e "\033[31mthe environment variable COULOMBLIB is set.OK.\033[0m"
