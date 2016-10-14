from . import Constants

import re
import os
import os.path

class DirectoryProcessor:
	@staticmethod
	def create(tracked_directory, database):
		return DirectoryProcessor(tracked_directory, database)

	def __init__(self, tracked_directory, database):
 		self.tracked_directory = tracked_directory
 		self.database = database

	def process(self):
		if not self.tracked_directory.is_directory():
			return

		directory_a_day_path = self.tracked_directory.get_directory_a_day_path()
		for file_path in self.tracked_directory.get_all_related_inner_file_paths():
			is_ignored = False

			for pattern in self.tracked_directory.get_ignore_regexes():
				if re.search(pattern, file_path):
					is_ignored = True

			if is_ignored:
				continue

			if not os.path.exists(directory_a_day_path):
				os.mkdir(directory_a_day_path)

			if not os.path.isdir(directory_a_day_path):
				print "The name that fc-helper wanted to use for a new date folder is taken by a file"
				return

			os.rename(self.tracked_directory.get_absolute_inner_file_path(file_path), \
				        os.path.join(directory_a_day_path, file_path))
