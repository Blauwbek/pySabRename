#pySabRename
pySabRename is a post-processing script for sabnzbd and nzbget.
It renames the biggest file in the final download folder to the job name. It will also rename subtitles and the nfo.
After renaming it will clean up the download dir.

##Why pySabRename
* pySabRename is written in Python, so it's usable on many OSs
* pySabRename also checks subfolders (I've not seen many spots placing the actual movie in a subfolder, but I've seen them)
* pySabRename is only a few lines of code
* pySabRename has builtin code for use with SickBeard
* pySabRename will only rename the files YOU want

##How to 'install'
###Sabnzbd
* Download pySabRename
* If you already have postprocessing scripts, place the script in the right folder
* If you dont, create a folder somewhere and place the script in that folder
* Goto http://your-sabnzbd-host:8080/sabnzbd/config/folders/ and set your postprocessing folder to said folder
* Optional: goto http://your-sabnzbd-host:8080/sabnzbd/config/categories/ and set the script for the cat's you want
* Select the postprocessing script on the overview

##Use
This program is used in sabnzbd and works really well when using the latest SpotWeb pull. It is designed for movies and tv episodes with 'encrypted' (=mostly random or flipped) filenames.

##Warning
It will not work as you'd probably like when multiple episodes are downloaded in the same job!

##Todo
* Test with NZBget on all platforms
