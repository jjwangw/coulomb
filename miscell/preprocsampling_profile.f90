subroutine preprocsampling_profile(profilename,nL,nW,extendLW,aftershockfilename,samplingprofilename)
!this fortran-style code is based on the m-script preprocsampling_profile.m from the AutoCoulomb program.
implicit none
!integer*4 nprofile,nL,nW
integer*4 nL,nW
!real*8 profilearray(nprofile,11)
real*8,allocatable::profilearray(:,:)
character*100 profilename,aftershockfilename,samplingprofilename
real*8 extendLW(4),ksi_range(2),eta_range(2)
!f2py intent(in)::profilename,nL,nW,extendLW,aftershockfilename,samplingprofilename
!
real*8 L,W,AL1,AL2,AW1,AW2,strike,dip,m2km
integer*4 i,j,k,nrow,NT
real*8 deg2rad,ksi0,eta0,z0,sB,sL,sL0,x0,y0
real*8 ksi,eta,x,y,z,Bc,Lc,n
!
real*8 result_fault_corners(6,3),dcheck1
real*8 k1,k2,k3,k4,temp,tempw
!
real*8, allocatable::LL(:),WW(:),LL0(:),WW0(:)
character*100 str
character*100 filenameout,dir,filename,extension
!
integer*4 naftershocksfile,bskip
!integer*4 naftershocks
integer*4 stat
!
NT=nL*nW
allocate(LL0(nL))
allocate(WW0(nW))
allocate(LL(NT))
allocate(WW(NT))
!%-------------------------------------------------------------------------%
open(100,file=profilename)
read(100,*)nrow
allocate(profilearray(nrow,11))
do i=1,nrow
   read(100,*)(profilearray(i,j),j=1,11)
!   write(*,*)(profilearray(i,j),j=1,11)
enddo
close(100)
!nrow=size(profilearray,1)
!
m2km=1.0e-3;
do i=1,nrow
    !sL0=lon(i);
    sL0=profilearray(i,2)
    !L=length(i);
    L=profilearray(i,4)
    !W=width(i);
    W=profilearray(i,5)
    AL1=profilearray(i,6)
    AL2=profilearray(i,7)
    AW1=profilearray(i,8)
    AW2=profilearray(i,9)
    if((AL2-AL1-L)>=1.0e-6 .or. (AW2-AW1-W)>=1.0e-6) then
       print*,'the format of the input file associated with profiles is wrong!'
       stop
    endif
    !strikee=strike(i);
    strike=profilearray(i,10)
    !dipp=dip(i);
    dip=profilearray(i,11)
    ksi0=abs(AL1);
    eta0=abs(AW1);
    z0=-profilearray(i,3);
    sB=profilearray(i,1);
    sL=profilearray(i,2);
    call generalBL2xy(sB,sL,sL0,3,1,x0,y0)
    x0=x0*m2km;!from meter to kilometer
    y0=y0*m2km;
    ! 
    !-----------------------------------!
    dcheck1=W*sin(deg2rad(dip)) - ( -z0+abs(AW1)*sin(deg2rad(dip)) )
    tempw=-z0/sin(deg2rad(dip))+abs(AW1)
    if(dcheck1>0)then
        print*,'warning: a wrong width! the upper edge of the fault plane is above the earth''s surface!'
        !W=-z0/sin(deg2rad(dip))+abs(AW1);
        W=tempw
    endif
    !ksi_range=[k1*L, k2*L];
    !eta_range=[k3*W,k4*W];
    k1=extendLW(1)
    k2=extendLW(2)
    k3=extendLW(3)
    k4=extendLW(4)
    if(k1.gt.k2)then
        temp=k2
        k2=k1
        k1=temp
    endif
    if(k3.gt.k4)then
        temp=k4
        k4=k3
        k3=temp
    endif
    ksi_range(1)=k1*L
    ksi_range(2)=k2*L
    eta_range(1)=k3*W
    eta_range(2)=k4*W
    if(eta_range(2)>tempw)then
       eta_range(2)=tempw !don't allow the uppermost edge of the profile to be above the earth
    endif
    !%-----------------------------------%
    !result_fault_corners=[];
    !for j=1:6
    do j=1,6
        select case(j)
        !switch j
            case(1) !the lower-left corner of the fault plane
                ksi=0.0
                eta=0.0
                n=0.0
            case(2) !the lower-right corner of the fault plane
                ksi=L
                eta=0.0
                n=0.0
            case(3) !the upper-right corner of the fault plane
                ksi=L
                eta=W
                n=0
            case(4) !the upper-left corner of the fault plane
                ksi=0
                eta=W
                n=0
            case(5) !the uppler-left corner of the projected plane along the updip direction
                ksi=0
                eta=-z0/sin(deg2rad(dip))+abs(AW1)
                n=0
            case(6) !the uppler-right corner of the projected plane along the updip direction
                ksi=L
                eta=-z0/sin(deg2rad(dip))+abs(AW1)
                n=0
        end select
        call faultplanecoord2localCartesiancoord(strike,dip,ksi0,eta0,x0,y0,z0,ksi,eta,n,x,y,z)
        x=x/m2km;!km to m
        y=y/m2km;
        call generalxy2BL(x,y,sL0,3,Bc,Lc);
        result_fault_corners(j,1)=Lc
        result_fault_corners(j,2)=Bc
        result_fault_corners(j,3)=z
 !       result_fault_corners=[result_fault_corners;Lc Bc z];
  enddo !end of loop j
!%-------------------------------------------------------------------------%
     call linspace(min(ksi_range(1),ksi_range(2)),max(ksi_range(1),ksi_range(2)),nL,LL0)
!    WW=linspace(min(eta_range),max(eta_range),NN);
     call linspace(min(eta_range(1),eta_range(2)),max(eta_range(1),eta_range(2)),nW,WW0)
!    [LL,WW]=meshgrid(LL,WW);
     call meshgrid(LL0,WW0,nL,nW,LL,WW)
!    LL=LL(:);
!    WW=WW(:);
!    pathout=['../profile/profile_along_fault_plane',num2str(i),'.txt'];
     write(str,'(i4)')i
     j=len(str)
     !print*,'j=',j
     !print*,'str=',str,'len(str)=',len(trim(str))
     if(len(trim(adjustl(samplingprofilename))).eq.0)then
        call parsefilename(profilename,dir,filename,extension)
     else
        call parsefilename(samplingprofilename,dir,filename,extension)
     endif
     if(extension=="")then
        extension='.txt'
     endif
     !print*,'extension=',extension,'trim(adjustl(str))=',trim(adjustl(str))
     filenameout=trim(adjustl(filename))//trim(adjustl(str))//trim(adjustl(extension))
     if(dir/="")then
        filenameout=trim(adjustl(dir))//'/'//filenameout
     endif
     !print*,'filenameout=',filenameout
     open(100,file=filenameout)
!     open(100,file=profilename//trim(adjustl(str)))
!    fp=fopen(pathout,'wt');
     write(100,*)'#The fault corners of a fault plane and the projected line on the earth''s & 
      & surface of the fault plane along updip direction.'
!    fprintf(fp,'%s\n','Fault corners of the fault plane and the projected line on the earth''s surface of the fault plane along updip direction.');
     write(100,*)'#In line 5 to 10, the 5th line is the lower left corner; the 6th line the lower right corner; &
     & the 7th line the upper right corner; the 8th corner the upper left corner.'
!    fprintf(fp,'%s\n','the 1st line: lower left corner; the 2nd line: lower right corner; the 3rd line:upper right corner; the 4th corner: upper left corner');
     write(100,*)'#The 9th line is the starting point of the projected line; the 10th line& 
     & the ending point of the projected line.'
!    fprintf(fp,'%s\n','the 5th line: the starting point of the projected line; the 6th line: the ending point of the projected line.');
     write(100,*)'#  lon(deg)       lat(deg)    depth(km)'
     do j=1,6
        write(100,1000) ( result_fault_corners(j,k),k=1,3)
     enddo
1000 format(3f13.6)
!    fprintf(fp,'%s\n','   lon(deg)       lat(deg)    depth(km)');
!    for ii=1:6
!        fprintf(fp,'%13.6f%13.6f%13.6f\n',temp(ii,1),temp(ii,2),temp(ii,3));
!    end
     write(100,*)'#The boundary coordinates on the profile:(ksi, W-eta(downdip km))'
     write(100,2000)ksi_range(1),eta_range(2)-eta_range(1)
     write(100,2000)ksi_range(2),eta_range(2)-eta_range(1)
     write(100,2000)ksi_range(2),0.0
     write(100,2000)ksi_range(1),0.0
2000 format(2f13.6)
     write(100,*)'#Sampling along strike and updip:',' nL=',nL,'nW=',nW
!    fprintf(fp,'%s\n','coordinate on the fault plane:(ksi, W-eta(downdip km))');
!    fprintf(fp,'%13.6f%13.6f\n%13.6f%13.6f\n%13.6f%13.6f\n%13.6f%13.6f\n',0,max(eta_range)-0,L,max(eta_range)-0,L,max(eta_range)-W,0,max(eta_range)-W);
     write(100,*)'#''Downdip'' means the reference point in the fault plane coordinate system is &
     &the upper left corner of the original profile whose extreme uppermost edge touches the earth''s surface.'
     write(100,*)'#The following are the sampling points on the fault plane (the single number in the following &
                 &line is the total number of sampling points on the profile):'
     write(100,*)'#     lat(deg)      lon(deg)       depth(km)       ksi(km)      W-eta(km)(downdip)'
     write(100,*)NT
!    fprintf(fp,'%s\n%s\n%d\n','The following are the sampling points on the fault plane','     lat(deg)    lon(deg)      depth(km)    ksi(km)      W-eta(km)(downdip)',NT);
!
     do k=1,NT
        ksi=LL(k)
        eta=WW(k)
        n=0
        call faultplanecoord2localCartesiancoord(strike,dip,ksi0,eta0,x0,y0,z0,ksi,eta,n,x,y,z)
        x=x/m2km
        y=y/m2km
        call generalxy2BL(x,y,sL0,3,Bc,Lc)
        write(100,3000)Bc,Lc,-z,ksi,eta_range(2)-eta
     enddo
3000 format(6f15.6)
!%-------------------------------------------------------------------------%
naftershocksfile=len(trim(adjustl(aftershockfilename)))
!print*,'naftershocksfile=',naftershocksfile
if(naftershocksfile.ne.0)then
    write(100,*)'#the projected coordinates of aftershocks on the profile:'
    write(100,*)'#     lat(deg)      lon(deg)       depth(km)       ksi(km)      W-eta(km)(downdip) normal(km)'
!    %
    open(200,file=aftershockfilename,iostat=stat)
    rewind(200) !rewind to the beginning of the file to prevent weird errors related to reading file 
     bskip=1
     do while(.TRUE.)
       if(bskip==1)then
          read(200,*,iostat=stat)str
          bskip=0
       else
         read(200,*,iostat=stat)sL,sB,z
         !write(*,*)'stat=',stat,'sL=',sL,'sB=',sB,'z=',z
         if(stat==0)then !to avoid doing twice when pointing to the end of the file 
           z=-z
           call generalBL2xy(sB,sL,sL0,3,1,x,y) 
           x=x*m2km
           y=y*m2km
           call localCartesiancoord2faultplanecoord(strike,dip,ksi0,eta0,x0,y0,z0,x,y,z,ksi,eta,n)
           write(100,4000)sB,sL,-z,ksi,eta_range(2)-eta,n
         endif
       endif ! bskip=1
       if(stat/=0) goto 30
    enddo
4000 format(6f15.6)
30 continue
endif
enddo !end of loop i
close(100)
close(200)
deallocate(profilearray)
deallocate(LL0)
deallocate(WW0)
deallocate(LL)
deallocate(WW)
end subroutine preprocsampling_profile
!---------------------------------------------------------------------------------------------!
function deg2rad(x)
implicit none
real*8 x,deg2rad
deg2rad=x/180.0*acos(-1.0)
end function deg2rad
!---------------------------------------------------------------------------------------------!
subroutine parsefilename(filenamein,dir,filename,extension)
character*100 filenamein,dir,filename,extension
integer*4 idot,jslash
idot=index(filenamein,'.',.TRUE.)
jslash=index(filenamein,'/',.TRUE.)
dir=trim(adjustl(filenamein(1:jslash-1)))
filename=trim(adjustl(filenamein(jslash+1:idot-1)))
extension=trim(adjustl(filenamein(idot:)))
!print*,'dir=',dir,'filename=',filename,'extension=',extension
end subroutine parsefilename
!---------------------------------------------------------------------------------------------!
subroutine linspace(x1,x2,n,y)
real*8 x1,x2
integer*4 n
real*8 y(n)
real*8 dx
dx=(x2-x1)/(n-1)
do i=1,n
   y(i)=x1+(i-1)*dx
enddo
end subroutine linspace
!---------------------------------------------------------------------------------------------!
subroutine meshgrid(x,y,m,n,xg,yg)
real*8 x(m),y(n),xg(m*n),yg(m*n)
integer*4 i,j,k
do j=1,m
  do i=1,n
       k=i+(j-1)*n
       xg(k)=x(j)
       yg(k)=y(i)
  enddo
enddo
end subroutine meshgrid
!---------------------------------------------------------------------------------------------!
subroutine AtimesB(A,B,C,m,n,s)
implicit none
real*8 A(m,n),B(n,s),C(m,s)
integer*4 m,n,s
integer*4 i,j,k
real*8 temp
do i=1,m
  do j=1,s
     temp=0.0
     do k=1,n
         temp=temp+A(i,k)*B(k,j)
     enddo
     C(i,j)=temp
  enddo
enddo
end subroutine AtimesB
!---------------------------------------------------------------------------------------------!
subroutine AplusB(A,B,C,m,n)
implicit none
real*8 A(m,n),B(m,n),C(m,n)
integer*4 m,n
integer*4 i,j
do i=1,m
 do j=1,n
     C(i,j)=A(i,j)+B(i,j)
 enddo
enddo
end subroutine AplusB
!---------------------------------------------------------------------------------------------!
subroutine faultplanecoord2localCartesiancoord(strike,dip,ksi0,eta0,x0,y0,z0,ksi,eta,n,x,y,z)
implicit none
real*8 strike,dip,ksi0,eta0,x0,y0,z0,ksi,eta,n,x,y,z
real*8 Rtheta(3,3),Rdip(3,3),temp1(3,3),temp2(3,1),temp3(3,1),temp4(3,1)
!f2py intent(in)::strike,dip,ksi0,eta0,x0,y0,z0,ksi,eta,n
!f2py intent(out)::x,y,z
!ksi,eta,n with reference point being the lower left corner of fault plane
real*8 theta,D,deg2rad
    theta=deg2rad(strike);
    D=deg2rad(dip);
!    Rtheta=[cos(theta)  sin(theta)  0;... %x north, y east, z upward
!            sin(theta) -cos(theta)  0;...
!            0            0          1];
    Rtheta(1,1)=cos(theta)
    Rtheta(1,2)=sin(theta)
    Rtheta(1,3)=0
    !
    Rtheta(2,1)=sin(theta)
    Rtheta(2,2)=-cos(theta)
    Rtheta(2,3)=0
    !
    Rtheta(3,1)=0
    Rtheta(3,2)=0
    Rtheta(3,3)=1.0
    !
!    Rdip=[1   0     0 ;...
!          0   cos(D) -sin(D);...
!          0   sin(D)  cos(D)];
    Rdip(1,1)=1.0
    Rdip(1,2)=0.0
    Rdip(1,3)=0.0
    !
    Rdip(2,1)=0.0
    Rdip(2,2)=cos(D)
    Rdip(2,3)=-sin(D)
    !
    Rdip(3,1)=0.0
    Rdip(3,2)=sin(D)
    Rdip(3,3)=cos(D)
    !
    !C=Rtheta*Rdip*[ksi-ksi0;eta-eta0;n]+[x0;y0;z0];
    !x=C(1);
    !y=C(2);
    !z=C(3);
    temp2(1,1)=ksi-ksi0
    temp2(2,1)=eta-eta0
    temp2(3,1)=n
    call AtimesB(Rtheta,Rdip,temp1,3,3,3)
    call AtimesB(temp1,temp2,temp3,3,3,1)
    temp2(1,1)=x0
    temp2(2,1)=y0
    temp2(3,1)=z0
    call AplusB(temp3,temp2,temp4,3,1)
    x=temp4(1,1);
    y=temp4(2,1);
    z=temp4(3,1);
end subroutine faultplanecoord2localCartesiancoord
!---------------------------------------------------------------------------------------------!
subroutine localCartesiancoord2faultplanecoord(strike,dip,ksi0,eta0,x0,y0,z0,x,y,z,ksi,eta,n)
!ksi,eta,n with reference point being the lower left corner of a fault plane
real*8 strike,dip,ksi0,eta0,x0,y0,z0,x,y,z,ksi,eta,n
!f2py intent(in)::strike,dip,ksi0,eta0,x0,y0,z0,x,y,z
!f2py intent(out)::ksi,eta,n
real*8 Rtheta(3,3),Rdip(3,3),temp1(3,3),temp2(3,1),temp3(3,1),temp4(3,1)
real*8 theta,D,deg2rad
    theta=deg2rad(strike);
    D=deg2rad(dip);
!    Rtheta=[cos(theta)  sin(theta)  0;... %x north, y east, z upward
!            sin(theta) -cos(theta)  0;...
!            0            0          1];
    Rtheta(1,1)=cos(theta)
    Rtheta(1,2)=sin(theta)
    Rtheta(1,3)=0.0
    !
    Rtheta(2,1)=sin(theta)
    Rtheta(2,2)=-cos(theta)
    Rtheta(2,3)=0.0
    !
    Rtheta(3,1)=0.0
    Rtheta(3,2)=0.0
    Rtheta(3,3)=1.0
    !
!    Rdip=[1   0     0 ;...
!          0   cos(D) -sin(D);...
!          0   sin(D)  cos(D)];
    Rdip(1,1)=1.0
    Rdip(1,2)=0.0
    Rdip(1,3)=0.0
    !
    Rdip(2,1)=0.0
    Rdip(2,2)=cos(D)
    Rdip(2,3)=-sin(D)
    !
    Rdip(3,1)=0.0
    Rdip(3,2)=sin(D)
    Rdip(3,3)=cos(D)
    !
    !A=Rdip'*Rtheta'*[x-x0;y-y0;z-z0]+[ksi0;eta0;0];
    call AtimesB(transpose(Rdip),transpose(Rtheta),temp1,3,3,3)
    temp2(1,1)=x-x0
    temp2(2,1)=y-y0
    temp2(3,1)=z-z0
    call AtimesB(temp1,temp2,temp3,3,3,1)
    temp2(1,1)=ksi0
    temp2(2,1)=eta0
    temp2(3,1)=0.0
    call AplusB(temp3,temp2,temp4,3,1)
    !ksi=A(1);
    !eta=A(2);
    !n=A(3);
    ksi=temp4(1,1)
    eta=temp4(2,1)
    n=temp4(3,1)
end subroutine localCartesiancoord2faultplanecoord
!---------------------------------------------------------------------------------------------!
