#!/usr/bin/python

from datetime import date
import glob
import json
import re
import syslog

import os
import os.path

APP_FOLDER = "/Library/Application Support/FolderControlder"
INFO_FILE  = "/info.json"

FOLDER_PATTERN = "^Folder-[0-9]{4}-[0-9]{2}-[0-9]{2}$"

def get_info_file():
	home = os.path.expanduser("~")
	# home = "~"
	path = home + APP_FOLDER + INFO_FILE

	return open(path, "r")

def process_folder(folder):
	path = os.path.expanduser(folder["path"] )

	if not os.path.isdir(path):
		print "It's not a dir, can't continue processing of this record"
		return

	len_of_path = len(path)
	list = [item[len_of_path + 1:] for item in glob.glob(path + "/*") ]

	ignore = folder["ignore"]
	ignore.append(FOLDER_PATTERN)

	today = date.today()
	date_folder = path + "/Folder-%04d-%02d-%02d" % (today.year, today.month, today.day)

	for item in list:
		is_ignored = False

		for pattern in ignore:
			if re.search(pattern, item):
				is_ignored = True

		if is_ignored:
			continue

		if not os.path.exists(date_folder):
			os.mkdir(date_folder)

		if not os.path.isdir(date_folder):
			print "The name that fc-helper wanted to use for a new date folder is taken by a file"
			return


		full_path = path + "/" + item
		destination = date_folder + "/" + item

		os.rename(full_path, destination)


if __name__ == "__main__":
	
	with get_info_file() as file:
		obj = json.load(file)

		for folder in obj["folders"]:
			process_folder(folder)

		
