from . import Constants

from datetime import date
import glob
import os
import os.path

class TrackedDirectory:
  @staticmethod
  def create(data):
    return TrackedDirectory(data)

  def __init__(self, data):
    self.path = os.path.expanduser(data[Constants.PATH_KEY])
    self.ignore_regexes = data[Constants.IGNORE_REGEXES_KEY] + [Constants.DIRECTORY_A_DAY_REGEX]

  def get_path(self):
    return self.path

  def get_ignore_regexes(self):
    return self.ignore_regexes

  def is_directory(self):
    return os.path.isdir(self.path)

  def get_all_related_inner_file_paths(self):
    return [file[len(self.path) + 1:] for file in glob.glob(self.path + "/*")]

  def get_directory_a_day_path(self):
    today = date.today()
    return os.path.join(self.path, Constants.DIRECTORY_A_DAY_TEMPLATE % (today.year, today.month, today.day))

  def get_absolute_inner_file_path(self, related_file_path):
    return os.path.join(self.path, related_file_path)
