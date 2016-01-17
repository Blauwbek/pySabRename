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
import subprocess

#config stuff
config = ConfigParser.RawConfigParser()
startfolder = os.path.dirname(sys.argv[0])
parexefile = os.path.join(os.path.dirname(sys.argv[0]), 'par2j.exe')
config.readfp(open(os.path.join(os.path.dirname(sys.argv[0]), 'pySR.cfg')))

#sab things
#dir the files are we want to use
final_dir = sys.argv[1]
#name to rename the biggest file to
job_name = sys.argv[3]
#user defined cat
job_cat = sys.argv[5]
#job result
job_res = sys.argv[7]

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
print '+------------------------------------------+'
print '| /Bitcoin Donations/:                     |'
print '+------------------------------------------+'
print '| To address:                              |'
print '| 14QFusmzBTAo9FhH7x7puHNkdCps8vamVV       |'
print '+------------------------------------------+'
print ''
print 'v2 - with par2 renaming for spotnet 1.8.x'
print ''
print '   _____             _              _     __   ___   _____       '
print '  / ____|           | |            | |   /_ | / _ \ | ____|      '
print ' | (___  _ __   ___ | |_ _ __   ___| |_   | || (_) || |__  __  __'
print "  \___ \| '_ \\ / _ \\| __| '_ \\ / _ \\ __|  | | > _ < |___ \ \\ \\/ /"
print '  ____) | |_) | (_) | |_| | | |  __/ |_   | || (_) | ___) | >  < '
print ' |_____/| .__/ \___/ \__|_| |_|\___|\__|  |_(_)___(_)____(_)_/\\_\\'
print '        | |                                                      '
print '        |_|                                                      '

if int(job_res) != 0:
	print 'To prevent bad stuff from happening we do not run this script on jobs that are not succesfully completed (par/rar fail)'
	print 'If you want to run this anyway try this in commandline:'
	print sys.argv[0], sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7]
	sys.exit(0)

par_file = ''

if not os.path.isdir(final_dir):
	print "Folder not found, exiting : ",final_dir
	sys.exit(0)

def find_par2(dir):
	global par_file, r_file
	for folder, subs, files in os.walk(dir):
		for item in files:
			filename, ext1 = os.path.splitext(item)
			item = os.path.join(folder, item)
			itemsize = os.path.getsize(item)
			if itemsize > r_file[1]:
				r_file = (item, itemsize)
			if ext1 == '.par2':
				par_file = item

find_par2(final_dir)

filename, ext = os.path.splitext(r_file[0])
print 'Found extension! ({})'.format(ext)

print "Script directory ",startfolder

if os.path.isfile(parexefile):
	if par_file != '':
		dir_name = os.path.dirname(par_file)
		file_name = os.path.basename(par_file)
		p_file = '"' + par_file + '"'
		print 'par2j: ' + p_file
		R=subprocess.call([parexefile,'r '+ p_file,'*'],cwd=dir_name)
		print 'Par2j Result=',R
		if R == 16:
			print 'par2j renaming done.'
			# get largest file to determine job-name
			r_file = ['',-1]
			find_par2 (final_dir)
			if r_file[1] > 0:
				job_name, ext = os.path.splitext(os.path.basename(r_file[0]))
				print "New jobname: " + job_name
else:
	print 'par2j.exe not found, skipped par2j renaming'

print "\n+Move / Renaming process+"
if r_file[1] != -1:
	filename = os.path.basename(r_file[0])
	print 'Found:', filename

old_name = r_file[0]
print 'Old name:', old_name

if any(ext == val for val in extlist):
	print 'Extention supported!', ext
	new_file = os.path.join(final_dir, job_name + ext)
	print 'New name:', new_file
	os.rename(old_name, new_file)
else:
	print 'This file has an extension that is not supported to prevent wrong renames like multi-file movies (dvds etc.):', ext
	sys.exit(0)

for s_ext in sublist:
	if os.path.isfile(filename + s_ext):
		os.rename(filename + s_ext, os.path.join(final_dir, job_name + s_ext))
		print 'We found and renamed a subtitle file with the extension', s_ext
# end of rename block

#do cleanup
def cleanup(top):
	global final_dir, job_name, ext, sublist
	print "\n+Cleaning process+"
	if top == '/' or top == '\\':
		print 'nope.jpg'
	else:
		for root, dirs, files in os.walk(top, topdown=False):
			for name in files:
				if not any(os.path.splitext(name)[1] == s_ext for s_ext in sublist) and not os.path.join(root, name) == os.path.join(final_dir, job_name + ext) and not os.path.splitext(name)[1] == '.nfo':
					os.remove(os.path.join(root, name))
					print 'Removed:', os.path.join(root, name)
			for name in dirs:
				try:
					os.rmdir(os.path.join(root, name))
					print 'Removed dir:', os.path.join(root, name)
				except:
					print 'Unable to delete dir:', os.path.join(root, name)

if config.get('sabnzbd', 'moviecat') == job_cat:
	if config.getboolean('movies', 'cleanup'):
		cleanup(final_dir)

if config.get('sabnzbd', 'tvcat') == job_cat:
	if config.getboolean('tv', 'cleanup'):
		cleanup(final_dir)

	if config.getboolean('tv', 'sickbeard'):
		print '\n+Calling Sickbeard+'
		try:
			import autoProcessTV
			
			if autoProcessTV.processEpisode.func_code.co_argcount == 2:
				autoProcessTV.processEpisode(final_dir, sys.argv[2])
			elif autoProcessTV.processEpisode.func_code.co_argcount == 3:
				autoProcessTV.processEpisode(final_dir, sys.argv[2], job_res)
		except:
			print 'Could not run sickbeard, is autoProcessTV in the same folder as this script?'

sys.exit(0)