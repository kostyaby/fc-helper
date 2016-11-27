from . import Constant
from . import SortingStrategyFactory

from datetime import date
import glob
import os
import re


class TrackedDirectory:
  def __init__(self, data, clock):
    self.path = os.path.expanduser(data[Constant.Config.PATH_KEY])
    self.sorting_strategy = SortingStrategyFactory.create(data[Constant.Config.SORTING_STRATEGY_KEY], clock)
    self.ignore_regexes = data[Constant.Config.IGNORE_REGEXES_KEY] + self.sorting_strategy.get_regexes_to_ignore()


  def is_directory(self):
    return os.path.isdir(self.path)


  def get_all_tracked_entity_paths(self):
    return [os.path.basename(file) for file in glob.glob(self.path + "/*")]


  def get_absolute_tracked_entity_path(self, tracked_entity_path):
    return os.path.join(self.path, tracked_entity_path)


  def validate_target_directory(self, target_directory_path):
    absolute_path = os.path.join(self.path, target_directory_path)

    if not os.path.exists(absolute_path):
      os.mkdir(absolute_path)

    if not os.path.isdir(absolute_path):
      print "Target directory's name is already taken by a plain file"
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
