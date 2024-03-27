!---------------------------------------------------------------------------------------------------!
!the following codes come from the 'AutoCoulomb' program
!Dec.22,2023 by jjwang
!---------------------------------------------------------------------------------------------------!
!compute coulomb stress changes via reading stress tensors from an input file and write results into another file.
subroutine computeCFS(stress_filename,coulomb_filename,strike,dip,rake,friction,skempton)
implicit none
character*100 stress_filename, coulomb_filename,strline
real*8 strike,dip,rake,friction,skempton
!f2py intent(in)::stress_filename
!f2py intent(in)::coulomb_filename
!f2py intent(in)::strike
!f2py intent(in)::dip
!f2py intent(in)::rake
!f2py intent(in)::friction
!f2py intent(in)::skempton
!
real*8 stress(6),shear_stress,normal_stress,coulomb_stress
integer*4 i,ncount
ncount=0
!
write(*,*)'-----the parameters of receiver faults-----'
write(*,*)strike,dip,rake,friction,skempton
open(10,file=stress_filename)
open(11,file=coulomb_filename)
write(*,*)'processing...'
write(11,*)'    shear_stress(bar)  normal_stress(bar) coulomb_stress(bar)'
do while(.true.)
   if(ncount.eq.0)then
    read(10,*)strline
   else
     read(10,*,end=100)(stress(i),i=1,6)
!     write(*,*)(stress(i),i=1,6)
     call CFF(stress,strike,dip,rake,friction,skempton,shear_stress,normal_stress,coulomb_stress)
     write(11,1000)shear_stress,normal_stress,coulomb_stress
!     1000 format(3e18.6)
     1000 format(3f20.8)
   endif
   ncount=1
enddo
100 close(10)
close(11)
!print*,trim(coulomb_filename)//' is generated.'
end
!---------------------------------------------------------------------------------------------------!
!compute coulomb stress changes via input parameters with the type of array or matrix in a batch-process fashion. 
 module CFSmod
  real*8,allocatable,dimension(:,:)::stress
  real*8,allocatable,dimension(:)::shearstress,normalstress,coulombstress
  real*8,allocatable,dimension(:)::strike,dip,rake,friction,skempton
 contains
  subroutine arrayCFS()
  real*8 tempstress(6),tempshear,tempnormal,tempcoulomb
  real*8 tempstrike,tempdip,temprake,tempfriction,tempskempton
  integer*4 nrowst,nrows,nrowd,nrowr,nrowf,nrowsk
  integer*4 i,j
  nrowst=size(stress,dim=1)
  nrows=size(strike)
  nrowd=size(dip)
  nrowr=size(rake)
  nrowf=size(friction)
  nrowsk=size(skempton)
!  print*,'friction(1)=',friction(1),'skempton(1)=',skempton(1)
!  print*,'nrowst=',nrowst,'nrows=',nrows,'nrowd=',nrowd,'nrowr=',nrowr,'nrowf=',nrowf,'nrowsk=',nrowsk
  !
  if((nrows.ne.nrowd).or.(nrowd.ne.nrowr)) then
     print*,'***the total rows of the strike, dip and rake angles should be the same.***'
     stop
  endif
  if(nrowf.ne.nrowsk) then
     print*,'***the total rows of the friction and skempton coefficents should be the same.***'
     stop
  endif
  if(nrows.gt.1)then
      if(nrowst.ne.nrows) then
        print*,'***the total rows of the stresses and the strike,dip and rake angles &
	&should be the same if multiple receiver faults are considered.***'
        stop
      endif
  endif
  if((nrowf.ne.1).and.(nrowf.ne.nrows)) then
       print*,'***the total row of the friction coefficient should be either one or equal to that of strike angles***'
       stop
  endif
  !
  do i=1,nrowst
   tempstrike=strike(1)
   tempdip=dip(1)
   temprake=rake(1)
   tempfriction=friction(1)
   tempskempton=skempton(1)
    if(nrows.gt.1)then
       tempstrike=strike(i)
       tempdip=dip(i)
       temprake=rake(i)
       if(nrowf.gt.1)then
         tempfriction=friction(i)
         tempskempton=skempton(i)
       endif
    endif
     do j=1,6
        tempstress(j)=stress(i,j)
     enddo
 !  print*,'i=',i,'tempstress(1)=',tempstress(1),'tempstress(2)=',tempstress(2)&
 !   ,'tempstrike=',tempstrike,'tempdip=',tempdip,'temprake=',temprake &
 !   ,'tempfriction=',tempfriction,'tempskempton=',tempskempton 
    call  CFF(tempstress,tempstrike,tempdip,temprake,tempfriction,tempskempton,&
          tempshear,tempnormal,tempcoulomb)
    shearstress(i)=tempshear
    normalstress(i)=tempnormal
    coulombstress(i)=tempcoulomb
 !  print*,'temp shear stress=',tempshear,'temp normal stress=',tempnormal,'temp coulomb stress=',tempcoulomb
 !  print*,'shear stress=',shearstress,'normal stress=',normalstress,'coulomb stress=',coulombstress
  enddo
  end
 end module CFSmod
!---------------------------------------------------------------------------------------------------!
!compute coulomb stress changes via input parameters at a single sampling point
subroutine CFF(stress,strike,dip,rake,friction,skempton,shear_stress,normal_stress,coulomb_stress)
!
implicit none
!
real*8 stress(6)
real*8 strike,dip,rake,friction,skempton
real*8 shear_stress,normal_stress,pore_pressure,coulomb_stress
real*8 e11,e12,e13,e22,e23,e33
real*8 phi,delta,lambdaa
real*8 deg2rad
!
!f2py intent(in)::stress
!f2py intent(in)::strike
!f2py intent(in)::dip
!f2py intent(in)::rake
!f2py intent(in)::friction
!f2py intent(in)::skempton
!f2py intent(out)::shear_stress
!f2py intent(out)::normal_stress
!f2py intent(out)::coulomb_stress
!
!
!deg2rad=acos(-1.0)/180.0
e11=stress(1)
e12=stress(2)
e13=stress(3)
e22=stress(4)
e23=stress(5)
e33=stress(6)
!
phi=deg2rad(strike)
delta=deg2rad(dip)
lambdaa=deg2rad(rake)
!
shear_stress=sin(lambdaa)*(-1.0/2.0*sin(phi)**2*sin(2*delta)*e11+1.0/2.0*sin(2*phi)*sin(2*delta)*e12+ &
              sin(phi)*cos(2*delta)*e13-1.0/2.0*cos(phi)**2*sin(2*delta)*e22-cos(phi)*cos(2*delta)*e23+1.0/2.0*sin(2*delta)*e33)+ &
            cos(lambdaa)*(-1.0/2.0*sin(2*phi)*sin(delta)*e11+cos(2*phi)*sin(delta)*e12+cos(phi)*cos(delta)*e13+ &
            1.0/2.0*sin(2*phi)*sin(delta)*e22+sin(phi)*cos(delta)*e23)
normal_stress=sin(phi)**2*sin(delta)**2*e11-sin(2*phi)*sin(delta)**2*e12-sin(phi)*sin(2*delta)*e13+ &
               cos(phi)**2*sin(delta)**2*e22+cos(phi)*sin(2*delta)*e23+cos(delta)**2*e33
pore_pressure=-skempton/3.0*(e11+e22+e33)
coulomb_stress=shear_stress+friction*(normal_stress+pore_pressure)
end
!---------------------------------------------------------------------------------------------------!
real*8 function  deg2rad(deg_angle)
implicit none
real*8 deg_angle
deg2rad=deg_angle/180.0*acos(-1.0)
end
!---------------------------------------------------------------------------------------------------!
