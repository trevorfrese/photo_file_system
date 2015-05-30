from subprocess import call
import sys
import os

argv = sys.argv

file_string = argv[2].split('.')[0]
print file_string

call(["split", "-b","30000", argv[1], "upload_pics/output_" + file_string])

files = []


for filename in os.listdir("./upload_pics"):
	if filename.startswith("output_" + file_string):
		files.append(filename)

files.sort()
count = 0
print files 
for filename in files:
	count += 1

	call(["java", "-jar","f5.jar", "e", "-e", "upload_pics/" + filename, argv[2], "upload_pics/" + file_string + "_"+ str(count) +  ".jpg"])

	os.remove("upload_pics/"+ filename)


os.system("python upload_pics/uploadr.py")