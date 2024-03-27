def colorstr(string,color='black'):
   '''
      input:
           string: a string.
	   color(optional): the color to be set for the string.
      output:
           the colored string.
      dependence:
           None
      usage:
           print(colorstr('test',color='red'))
      version:
           v1.0 Dec.30,2023 by jjwang
             
   '''
   bcolor=0
   if color=='black':
      tempstr='\033[30m'+string+'\033[0m'
      bcolor=1
   if color=='red':
      tempstr='\033[31m'+string+'\033[0m'
      bcolor=1
   if color=='green':
      tempstr='\033[32m'+string+'\033[0m'
      bcolor=1
   if color=='blue':
      tempstr='\033[34m'+string+'\033[0m'
      bcolor=1
   if color=='pink':
      tempstr='\033[35m'+string+'\033[0m'
      bcolor=1
   if color=='cyan':
      tempstr='\033[36m'+string+'\033[0m'
      bcolor=1
   if bcolor==0:
      raise Exception('\033[91mthe given color is not coped with.\033[0m')
   return tempstr
if __name__=='__main__':
   print(colorstr('test'))
   print(colorstr('test','pink'))
  
