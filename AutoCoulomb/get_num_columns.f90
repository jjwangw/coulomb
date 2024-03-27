subroutine get_num_columns(filename,nskips,nmax,ncol)
!coded on Sep. 27,2021 by jjwang
!modified on Jan.2,2023 by jjwang
!filename:a file name 
!nskips:the target line of which columns are to be counted.
!nmax: the maximum length for a buffer to store the target line, say 200
!ncol: the return parameter of the number of columns for the target line
implicit none
integer*4 nskips,nmax,nstr,i,j,k,ncol,nstate
character(len=100)::filename
character(len=nmax)::str,tempstr
if(nmax.lt.0)then
  stop 'error: nmax is negative.'
endif
open(100,file=filename)
!skipping nskips-1 lines
!do i=1,nskips-1
do i=1,nskips
    read(100,'(a)')tempstr
!   tempstr=trim(tempstr)
!   write(*,*)'tempstr=',tempstr
end do
!read the end line of all nskips lines
read(100,'(a)')str
!write(*,*)'str=',str
str=trim(str)
!write(*,*)'str=',str
nstr=len(str)
ncol=0
j=0
do i=1,nstr-1
!  if( str(i:i)/=' '.and.(str(i+1:i+1)==' '.or.str(i+1:i+1)=='\0') ) then
!    ncol=ncol+1
!endif
read(str,*,iostat=nstate)(tempstr,k=1,i)
if (nstate/=0) then
    ncol=i-1
    exit
endif
end do
close(100)
end subroutine get_num_columns
