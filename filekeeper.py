#!/usr/bin/env python
import os,sys
import argparse
import pwd,grp
import socket
import platform
import time
import json
from shutil import copyfile


def localbackup(hostname,fname,stats,backupPath):
	'''
	Compare st_mtime
	'''
	st_mtime 	= stats[hostname][os.path.abspath(fname)]['st_mtime']
	backup_path 	= '%s%s%s_%s'%(backupPath,hostname,os.path.abspath(fname),st_mtime)
	dirname 	= os.path.split(backup_path)[0]

	if not os.path.isdir(dirname):
		os.makedirs(dirname)

	if not os.path.isfile(backup_path):
		copyfile(os.path.abspath(fname),backup_path)


def getFileStats(fname):
	'''
	Return a Dict with the OS stat of the given file
	'''
	try:
		fname = os.path.abspath(fname)
		s = os.stat(fname)
		stats = {}
		if platform.system() == 'Darwin' or platform.system() == 'Linux':
			stats[socket.gethostname()] 			= {}
			stats[socket.gethostname()]['timestamp']	= int(time.time())
			stats[socket.gethostname()][fname] 		= {}
			stats[socket.gethostname()][fname]['st_mode'] 	= s[0]
			stats[socket.gethostname()][fname]['st_ino'] 	= s[1]
			stats[socket.gethostname()][fname]['st_dev'] 	= s[2]
			stats[socket.gethostname()][fname]['st_nlink'] 	= s[3]
			stats[socket.gethostname()][fname]['st_uid'] 	= pwd.getpwuid(s[4])[0]
			stats[socket.gethostname()][fname]['st_gid'] 	= grp.getgrgid(s[5])[0]
			stats[socket.gethostname()][fname]['st_size'] 	= s[6]
			stats[socket.gethostname()][fname]['st_atime'] 	= s[7]
			stats[socket.gethostname()][fname]['st_mtime'] 	= s[8]
			stats[socket.gethostname()][fname]['st_ctime'] 	= s[9]
		else:
			raise Exception("Error: %s is not a supported OS"%(platform.system()))
		return stats
	except Exception as ex:
		print "%s"%(str(ex))
		sys.exit()

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-f", "--file",   	dest = "FilenameWatch", help = "File to check for changes", metavar = "FILE")
	parser.add_argument("-b","--backup",	dest = "BackupPath",	help = "Backup path", default = "/backups/filekeeper/")
	args = parser.parse_args()
	file_statistics = {}
	hostname = None
	file_statistics = getFileStats(fname = args.FilenameWatch)
	backup_path 	= args.BackupPath
	for h in file_statistics:
		hostname = h
	if args.FilenameWatch:
		localbackup(hostname = hostname, fname = args.FilenameWatch, stats = file_statistics, backupPath = backup_path)
