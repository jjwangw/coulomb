#!/usr/bin/env bash
fortran_files=`ls *.f* | sed -n 'H;${x;s/\n/ /g;p;}'`
fortran_files=$(echo "$fortran_files" | sed s/^' '//)
echo "fortran_files=$fortran_files"
f2py -c $fortran_files -m autocoulomb
#f2py -c AutoCoulomb.f90 CFF.f90 GradientDisp2Strain.f90 InitializeStress.f90 Rphi.f90 Strain2Stress.f90 StressArray2StressTensor.f90 StressTensor2StressArray.f90 TensorTrans.f90 deg2rad.f90 generalBL2xy.f90 generalxy2BL.f90 get_num_columns.f90 lonlat2xy.f90 -m autocoulomb
 #  autocoulomb.cpython-39-darwin.so
mv autocoulomb.*.so autocoulomb.so
cp autocoulomb.so  ../../coulomb/
