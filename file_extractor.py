from subprocess import call
import sys
import os

def extract_file(fname):
	image_name = fname.split('.')[0]
	print image_name

	outfile = open('output_file_finished', 'w+')

	files = []
	for filename in os.listdir("."):
		if filename.startswith(image_name + "_"):
			files.append(filename)

	files.sort()

	outfiles = []
	count = 1
	for filename in files:
		call(["java", "-jar","f5.jar", "x", "-e", "output_file" + str(count), filename])
		outfiles.append("output_file" + str(count))
		count+=1
		call(["cat", "output_file" + str(count), "> output_file_finished"])

	#full_list_of_files = ' '.join(outfiles)
	#call(["cat", full_list_of_files])


if __name__ == "__main__":
	extract_file(sys.argv[1])