from subprocess import call
import sys
import os

argv = sys.argv

image_name = argv[2].split('.')[0]
print image_name

call(["split", "-b","4096", argv[1], "output_" + image_name])

files = []

for filename in os.listdir("."):
	if filename.startswith("output_" + image_name):
		files.append(filename)

files.sort()
count = 0 
for filename in files:
	count += 1

	call(["java", "-jar","f5.jar", "e", "-e", filename, argv[2], image_name + "_"+ str(count) +  ".jpg"])

	os.remove(filename)




