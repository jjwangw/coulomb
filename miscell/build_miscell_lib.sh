#!/usr/bin/env bash
#fortran_files=`ls *.f* | sed -n 'H;${x;s/\n/ /g;p;}'`
#fortran_files=$(echo "$fortran_files" | sed s/^' '//)
#echo "fortran_files=$fortran_files"
fortran_files="sampling_points_given_depth.f90 generalBL2xy.f90 generalxy2BL.f90"
f2py -c $fortran_files -m samplingpointsgivendepth
mv samplingpointsgivendepth.*.so samplingpointsgivendepth.so
cp samplingpointsgivendepth.so  ../coulomb/
#
fortran_files=preprocsampling_profile.f90
f2py -c $fortran_files -m preprocsampling_profile
mv preprocsampling_profile.*.so preprocsampling_profile.so
cp preprocsampling_profile.so ../coulomb/
