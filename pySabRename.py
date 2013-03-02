#!/usr/bin/python
import sys
import os

#sab things
#dir the files are we want to use
final_dir = sys.argv[1]
#name to rename the biggest file to
job_name = sys.argv[3]

#non-sab things
#largest file so far and size, for use in find(dir)
r_file = ("", -1)

#got this from http://bit.ly/13qeOvk
def find(dir):
	print "Searching dir: ", dir
	global r_file
	for item in os.listdir(dir):
		item = dir + "/" + item
		if os.path.isdir(item):
			find(item)
		else:
			itemsize = os.path.getsize(item)
			if itemsize > r_file[1]:
				r_file = (item, itemsize)

find(final_dir)
if r_file[1] != -1:
	print "Found: ", os.path.basename(r_file[0])

old_name = r_file[0]
print "Old name: ", old_name

ext = os.path.splitext(r_file[0])[1]
print "Found extention! ({})".format(ext)

new_file = final_dir+ "\\" + job_name + ext
print "New name: {}".format(new_file)
os.rename(old_name, new_file)

sys.exit(0)