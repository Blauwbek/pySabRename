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
import ConfigParser

#config stuff
config = ConfigParser.RawConfigParser()
config.readfp(open(os.path.join(os.path.dirname(sys.argv[0]), 'pySR.cfg')))

#nzbget things
#dir the files are we want to use
final_dir = os.getenv('NZBPP_DIRECTORY')
#name to rename the biggest file to
job_name = os.getenv('NZBPP_NZBNAME')
#user defined cat
job_cat = os.getenv('NZBPP_CATEGORY ')
#job result
job_res = os.getenv('NZBPP_TOTALSTATUS')

#non-sab things
#largest file so far and size, for use in find(dir)
r_file = ('', -1)

#file extensions, edit at will
extlist = config.get('Static', 'vidext').split(',')
#subtitle extensions, also open for additions
sublist = config.get('Static', 'subext').split(',')


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

if job_res != 'SUCCESS':
	print 'To prevent bad stuff from happening we do not run this script on jobs that are not succesfully completed (par/rar fail)'
	sys.exit(95)

def find(dir):
	print "Searching dir: ", dir
	global r_file
	for item in os.listdir(dir):
		item = os.path.join(dir, item)
		if os.path.isdir(item):
			find(item)
		else:
			itemsize = os.path.getsize(item)
			if itemsize > r_file[1]:
				r_file = (item, itemsize)

find(final_dir)
print "\n+Renaming process+"
if r_file[1] != -1:
	filename = os.path.basename(r_file[0])
	print 'Found:', filename

old_name = r_file[0]
print 'Old name:', old_name

filename, ext = os.path.splitext(r_file[0])
print 'Found extension! ({})'.format(ext)

if any(ext == val for val in extlist):
	print 'Extention supported!', ext
	new_file = os.path.join(final_dir, job_name+ext)
	print 'New name:', new_file
	os.rename(old_name, new_file)
else:
	print 'This file has an extension that is not supported to prevent wrong renames like multi-file movies (dvds etc.):', ext
	sys.exit(95);

for s_ext in sublist:
	if os.path.isfile(filename+s_ext):
		os.rename(filename+s_ext, os.path.join(final_dir, job_name+s_ext))
		print 'We found and renamed a subtitle file with the extension', s_ext

def cleanup(top):
	global final_dir, job_name, ext, sublist
	print "\n+Cleaning process+"
	if top == '/' or top == '\\':
		print 'nope.jpg'
	else:
		for root, dirs, files in os.walk(top, topdown=False):
			for name in files:
				if not any(os.path.splitext(name)[1] == s_ext for s_ext in sublist) and not os.path.join(root, name) == os.path.join(final_dir, job_name+ext) and not os.path.splitext(name)[1] == '.nfo':
					os.remove(os.path.join(root, name))
					print 'Removed:', os.path.join(root, name)
			for name in dirs:
				try:
					os.rmdir(os.path.join(root, name))
					print 'Removed dir:', os.path.join(root, name)
				except:
					print 'Unable to delete dir:', os.path.join(root, name)
					sys.exit(94)

if config.get('sabnzbd', 'moviecat')==job_cat:
	if config.getboolean('movies', 'cleanup'):
		cleanup(final_dir)

if config.get('sabnzbd', 'tvcat')==job_cat:
	if config.getboolean('tv', 'cleanup'):
		cleanup(final_dir)

	if config.getboolean('tv', 'sickbeard'):
		print '\n+Calling Sickbeard+'
		
		nzbname = os.getenv('NZBPP_NZBFILENAME')
		
		try:
			import autoProcessTV
			
			if autoProcessTV.processEpisode.func_code.co_argcount == 2:
				autoProcessTV.processEpisode(final_dir, nzbname)
			elif autoProcessTV.processEpisode.func_code.co_argcount == 3:
				autoProcessTV.processEpisode(final_dir, nzbname, job_res)
		except:
			print 'Could not run sickbeard, is autoProcessTV in the same folder as this script?'
			sys.exit(94)

sys.exit(93)
