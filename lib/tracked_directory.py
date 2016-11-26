from . import Constant

from datetime import date
import glob
import os
import os.path
import re


class TrackedDirectory:
  def __init__(self, data):
    self.path = os.path.expanduser(data[Constant.Config.PATH_KEY])
    self.ignore_regexes = data[Constant.Config.IGNORE_REGEXES_KEY] + [Constant.Config.DIRECTORY_A_DAY_REGEX]


  def is_directory(self):
    return os.path.isdir(self.path)


  def get_all_tracked_entity_paths(self):
    return [os.path.basename(file) for file in glob.glob(self.path + "/*")]


  def get_absolute_tracked_entity_path(self, tracked_entity_path):
    return os.path.join(self.path, tracked_entity_path)


  def validate_directory_a_day(self, directory_a_day_path):
    directory_a_day_absolute_path = os.path.join(self.path, directory_a_day_path)

    if not os.path.exists(directory_a_day_absolute_path):
      os.mkdir(directory_a_day_absolute_path)

    if not os.path.isdir(directory_a_day_absolute_path):
      print "The name that fc-helper wanted to use for a new date folder is taken by a file"
      return False
      
    return True


  def is_ignored_tracked_entity(self, tracked_entity_path):
    for pattern in self.ignore_regexes:
      if re.search(pattern, tracked_entity_path):
        return True

    return False


  def crawl_directory(self):
    tracked_entities = {}
    for tracked_entity_path in self.get_all_tracked_entity_paths():
      if not self.is_ignored_tracked_entity(tracked_entity_path):
        tracked_entities[(self.path, tracked_entity_path)] = True

    return tracked_entities
