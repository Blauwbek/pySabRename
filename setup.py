from distutils.core import setup
import py2exe

setup(
	console=['pySabRename_win_dist.py'],
	zipfile=None,
	options={"py2exe":{"bundle_files": 1}}
	)
