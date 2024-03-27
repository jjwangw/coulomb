subroutine  SamplingPointsGivenDepth(minlon,maxlon,dLon,minLat,maxLat,dLat,depth,outputfile)
!original: Oct.15,2022 by jjwang
!modified: Jan.4,2023 by jjwang
implicit none
real*8 minLon,maxLon,dLon,minLat,maxLat,dLat
character*100 outputfile
!f2py 
!real*8 tempLon,tempLat,tempLon_bk,tempLat_bk
real*8 lon,lat,depth,temp,eps
!integer*4 narg,Nlines,nrow,ncol,nflag,ncount
!integer*4 i,j,narg,Nlines,nrow,ncol
integer*4 i,j,Nlines,nrow,ncol
integer*4 nflag
!
if(maxLat.lt.minLat)then
temp=maxLat
maxLat=minLat
minLat=temp
endif
!
if(maxLon.lt.minLon)then
temp=maxLon
maxLon=minLon
minLon=temp
endif
!
eps=1.0e-06
!if dLon=0 or dLat=0
if(abs(dLon).le.eps.or.abs(dLat).le.eps)then
print*,'error: dLon=',dLon,'dLat=',dLat,'Both should be larger than zero.'
stop
endif
!
nrow=floor( (maxLat-minLat)/dLat )
ncol=floor( (maxLon-minLon)/dLon )
nrow=nrow+1
ncol=ncol+1
Nlines=nrow*ncol
open(11,file=outputfile)
write(11,900)Nlines
900 format(i8)
!
nflag=0
if(nflag.eq.0)then !sampling latitude first and then longitude
 do j=1,ncol
   lon=minLon+(j-1)*dLon
   if(j.eq.ncol)then
      lon=maxLon
   endif
do i=1,nrow
   lat=minLat+(i-1)*dLat
   if(i.eq.nrow)then
      lat=maxLat
   endif
   write(11,1000)lat,lon,depth
enddo
enddo
else !or sampling longitude first and then latitude
!------------------
do i=1,nrow
   lat=minLat+(i-1)*dLat
   if(i.eq.nrow)then
      lat=maxLat
   endif
 do j=1,ncol
   lon=minLon+(j-1)*dLon
   if(j.eq.ncol)then
      lon=maxLon
   endif
   write(11,1000)lat,lon,depth
enddo
enddo
endif
1000 format(1x,3f13.6)
close(11)
end subroutine SamplingPointsGivenDepth
