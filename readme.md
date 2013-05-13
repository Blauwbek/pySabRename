#pySabRename
pySabRename is a post-processing script for sabnzbd.
It renames the biggest file in the final download folder to the job name.

##pySabRename vs sabRename
* pySabRename is written in Python, sabRename is written in C++
* pySabRename also checks subfolders (I've not seen many spots placing the actual movie in a subfolder, but I've seen them), sabRename doesn't
* pySabRename is multi OS, sabRename uses Windows.h (not exactly multi OS)
* pySabRename's py2exe is 4.76MB, sabRename.exe is 15,0kB

##Use
This program is used in sabnzbd and works really well when using the latest SpotWeb pull. It is designed for (mostly) movies with 'encrypted' (=mostly random or flipped) filenames.

##OS
This software can be used on any os running python (I might upload a py2exe dist).

##Todo
* Never really coded python before, if some more experienced python-coders could review it, that'd be great.
* Added functionality is always welcome