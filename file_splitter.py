from subprocess import call, Popen, PIPE, 
import sys
import os

def split_file(fname, imgfname):

	image_name = imgfname.split('.')[0]
	print image_name

	call(["split", "-b","131072", fname, "output_" + image_name])

	files = []
	for filename in os.listdir("."):
		if filename.startswith("output_" + image_name):
			files.append(filename)
	files.sort()

	count = 0
	for filename in files:
		count += 1

		p = call(["java", "-jar","f5.jar", "e", "-e", filename, imgfname, image_name + "_" + str(count) +  ".jpg"])

		os.remove(filename)

if __name__ == "__main__":
	split_file(sys.argv[1], sys.argv[2])