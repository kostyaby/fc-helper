from . import Constant

import glob
import os
import shutil

class Mover:
  def __init__(self, database, clock):
    self.database = database
    self.clock = clock


  def get_all_inner_entity_paths(self, path):
    return [os.path.basename(file) for file in glob.glob(path + "/*")]


  def merge_directories(self, old_absolute_path, new_absolute_path):
    unmerged_inner_entity_paths = []
    for inner_entity_path in self.get_all_inner_entity_paths(old_absolute_path):
      old_absolute_file_path = os.path.join(old_absolute_path, inner_entity_path)
      new_absolute_file_path = os.path.join(new_absolute_path, inner_entity_path)
      if not os.path.exists(new_absolute_file_path):
        os.rename(old_absolute_file_path, new_absolute_file_path)
      else:
        unmerged_inner_entity_paths.append(inner_entity_path)

    return unmerged_inner_entity_paths


  def move(self, tracked_directory, unsorted_tracked_entities):
    for tracked_entity in unsorted_tracked_entities:
      if self.clock.delta(tracked_entity.updated_at) <= Constant.Clock.UNSORTED_TO_SORTED_THRESHOLD_MILLIS:
        continue

      directory_a_day_path = self.clock.get_directory_a_day_path(tracked_directory)
      
      if tracked_directory.validate_directory_a_day(directory_a_day_path):
        old_related_path = tracked_entity.related_path
        new_related_path = os.path.join(directory_a_day_path, tracked_entity.related_path)

        old_absolute_path = os.path.join(tracked_directory.path, old_related_path)
        new_absolute_path = os.path.join(tracked_directory.path, new_related_path)

        try:
          os.rename(old_absolute_path, new_absolute_path)
        except OSError:
          unmerged_inner_entity_paths = self.merge_directories(old_absolute_path, new_absolute_path)

          if len(unmerged_inner_entity_paths) > 0:
            new_related_path = os.path.join(directory_a_day_path,\
                                            self.clock.get_timestamped_directory_name(tracked_entity.related_path))
            new_absolute_path = os.path.join(tracked_directory.path, new_related_path)
            os.rename(old_absolute_path, new_absolute_path)
          else:
            shutil.rmtree(old_absolute_path)

        tracked_entity.related_path = new_related_path
        tracked_entity.status = Constant.TrackedEntity.IGNORED_OR_MISSED
        self.database.update_tracked_entity(tracked_entity)
