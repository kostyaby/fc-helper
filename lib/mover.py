from . import Constant

import filecmp
import glob
import os
import shutil

class Mover:
  def __init__(self, database):
    self.database = database


  def get_all_inner_entity_paths(self, path):
    return [os.path.basename(file) for file in glob.glob(path + "/*")]


  def merge_directories(self, old_absolute_path, new_absolute_path):
    unmerged_inner_entity_paths = []
    for inner_entity_path in self.get_all_inner_entity_paths(old_absolute_path):
      old_absolute_file_path = os.path.join(old_absolute_path, inner_entity_path)
      new_absolute_file_path = os.path.join(new_absolute_path, inner_entity_path)
      if not os.path.exists(new_absolute_file_path):
        os.rename(old_absolute_file_path, new_absolute_file_path)
      elif os.path.isfile(old_absolute_file_path) and filecmp.cmp(old_absolute_file_path, new_absolute_file_path):
        os.remove(old_absolute_file_path)
      else:
        unmerged_inner_entity_paths.append(inner_entity_path)

    return unmerged_inner_entity_paths


  def move(self, tracked_directory, unsorted_tracked_entities):
    sorting_strategy = tracked_directory.sorting_strategy
    for tracked_entity in unsorted_tracked_entities:
      if sorting_strategy.should_be_skipped(tracked_entity):
        continue

      target_directory_path = sorting_strategy.get_target_directory_path(tracked_entity)
      
      if tracked_directory.validate_target_directory(target_directory_path):
        old_related_path = tracked_entity.related_path
        new_related_path = os.path.join(target_directory_path, tracked_entity.related_path)

        old_absolute_path = tracked_entity.get_absolute_path()
        new_absolute_path = os.path.join(tracked_directory.path, new_related_path)

        try:
          os.rename(old_absolute_path, new_absolute_path)
        except OSError:
          unmerged_inner_entity_paths = self.merge_directories(old_absolute_path, new_absolute_path)

          if len(unmerged_inner_entity_paths) > 0:
            new_related_path = os.path.join(target_directory_path,\
                                            sorting_strategy.avoid_naming_collisions(tracked_entity.related_path))
            new_absolute_path = os.path.join(tracked_directory.path, new_related_path)
            os.rename(old_absolute_path, new_absolute_path)
          else:
            shutil.rmtree(old_absolute_path)

        self.database.delete_tracked_entity(tracked_entity)
