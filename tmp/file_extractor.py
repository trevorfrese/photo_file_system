from subprocess import call
import sys
import os

argv = sys.argv

file_string = argv[1].split('.')[0]
print file_string

outfile = open('output_file_finished', 'w+')

files = []

for filename in os.listdir("."):
	if filename.startswith(file_string + "_"):
		files.append(filename)

file_num = len(files)

outfiles = []
count = 1
string_for_cat = "cat "
for i in range(file_num):
	filename = file_string + "_" + str(i + 1) + ".jpg"
	call(["java", "-jar","f5.jar", "x", "-e", "output_file" + str(count), filename])
	outfiles.append("output_file" + str(count))
	string_for_cat = string_for_cat + "output_file" + str(count)
	count+=1


string_for_cat = string_for_cat + " > out_file_finished" #we need to change this to mp3 manually right now
os.system(string_for_cat)
print string_for_cat
os.system("rm " + file_string + "_*")
os.system("rm output_*")

print files

#full_list_of_files = ' '.join(outfiles)

#call(["cat", full_list_of_files])