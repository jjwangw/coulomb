#!/usr/bin/env bash
usage(){
echo " "
echo -e "\033[31mUsage\033[0m: combined_profilegrids_profileCFS.sh   <[-G|--samplinggrids]>  <samplinggridsfile>  <[-C|--coulomb]>  <coulombfile>  [ <[-O|--outputfile]>  <outputfile> ]"
echo " "
echo -e "\
\033[31m-G samplinggrids\033[0m is the filename of a sampling profile. This file is generated using the python function 
    'samplingprofile' from the script of miscellan.py. 
\033[31m-C coulombfile]\033[0m is the filename of a coulomb stress file. This file is generated using the python function 'AutoCoulomb'
    from the script of AutoCoulomb.py
\033[31m-O outputfile]\033[0m is the filename of the combined file with the first two columns coming from the first two ones of the 
    sampling profile and the remaining three columns coming from the last three ones of the coulomb stress file."
 exit 0
 }
if [ $# -ne 6 ];then
  usage
fi
while true
do
  case "$1" in
      -G|--samplinggrids)
        samplinggridsfile=$2
        shift 2
        ;;
      -C|--coulomb)
        coulombfile=$2
        shift 2
        ;;
      -O|--outputfile)
        outputfile=$2
        shift 2
        ;;
      *)
       echo -e "\033[31m******wrong options!******\033[0m"
       usage
       exit 1
   esac
   if [ $# -eq 0 ];then
       break;
   fi
done
if [ -z "$samplinggridsfile" ];then
  echo ""
  echo -e "\033[31mthere is no sampling file.\033[0m"
  exit 1
  echo ""
fi
if [ -z "$coulombfile" ];then
  echo ""
  echo -e "\033[31mthere is no coulomb file.\033[0m"
  exit 1
  echo ""
fi
if [ -z "$outputfile" ];then
  echo ""
  echo -e "\033[31mthe output filename is not set.\033[0m"
  exit 1
  echo ""
fi
randomnumber="$RANDOM"
grids_filename=grids"$randomnumber"
coulomb_filename=coulomb"$randomnumber"
combined_filename=combined"$randomnumber"
sed '1,2d' $samplinggridsfile | awk '{print $4,$5}' > $grids_filename
sed '1d' $coulombfile | awk '{print $3,$4,$5}' > $coulomb_filename
paste $grids_filename $coulomb_filename > $combined_filename
echo " along_strike(km) along_downdip(km)   shear_stress(bar)   normal_stress(bar)   coulomb_stress(bar)"> $outputfile
cat $combined_filename >> $outputfile
rm $grids_filename $coulomb_filename $combined_filename
echo -e "\033[36m$outputfile is generated.\033[0m"
