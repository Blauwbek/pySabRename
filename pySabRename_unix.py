#! /usr/bin/python

# pySabRename
# Copyright (C) 2013  Blauwbek
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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


print 'pySabRename\n'
print '             _____       _    ______'
print '            /  ___|     | |   | ___ \\'
print ' _ __  _   _\\ `--.  __ _| |__ | |_/ /___ _ __   __ _ _ __ ___   ___'
print '| \'_ \\| | | |`--. \\/ _` | \'_ \\|    /| _ \\ \'_ \\ / _` | \'_ ` _ \\ / _ \\'
print '| |_) | |_| /\\__/ / (_| | |_) | |\\ \\| __/ | | | (_| | | | | | |  __/'
print '| .__/ \\__, \\____/ \\__,_|_.__/\\_| \\_\\___|_| |_|\\__,_|_| |_| |_|\\___|'
print '| |     __/ |'
print '|_|    |___/'
print ''
print ''
print '+------------------------------------------+'
print '| /Bitcoin Donations/:                     |'
print '+------------------------------------------+'
print '| To address:                              |'
print '| 14QFusmzBTAo9FhH7x7puHNkdCps8vamVV       |'
print '+------------------------------------------+'

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
	print 'Found: ', os.path.basename(r_file[0])

old_name = r_file[0]
print 'Old name: ', old_name

ext = os.path.splitext(r_file[0])[1]
print 'Found extension! ({})'.format(ext)

new_file = final_dir+ '/' + job_name + ext
print 'New name: ', format(new_file)
os.rename(old_name, new_file)

sys.exit(0)