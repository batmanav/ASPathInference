import os
import sys

if len(sys.argv) < 3:
        print "Usage: python generate_txt.py <from_folder> <to_folder>"
        exit()

folderstart=sys.argv[1]
folderend=sys.argv[2]

print "generating txt file for folder from "+str(folderstart)+" to "+str(folderend)

for folder in range(int(folderstart), (int(folderend)+1)):
	folder_path='./'+str(folder)
	for file in os.listdir(folder_path):
        	if file.endswith(".bin"):
                	print folder_path+' '+file
	                file_no_ext =  os.path.splitext(file)[0]
	                file_path=str(folder)+'/'+file
	                save_path=str(folder)+'/'+file_no_ext+'.txt'
					#cat RIB01.bin | ./../zebra-dump-parser/zebra-dump-parser.pl >RIB01.txt
	                command = 'cat '+file_path+' | ./zebra-dump-parser/zebra-dump-parser.pl > '+save_path
					print command
	                os.system(command)

