from subprocess import call
import sys
import os

argv = sys.argv

file_string = argv[2].split('.')[0]
print file_string

call(["split", "-b","4096", argv[1], "output_" + file_string])

files = []


for filename in os.listdir("."):
	if filename.startswith("output_" + file_string):
		files.append(filename)

files.sort()
count = 0
for filename in files:
	count += 1

	call(["java", "-jar","f5.jar", "e", "-e", filename, argv[2], file_string + "_"+ str(count) +  ".jpg"])

	os.remove(filename)




