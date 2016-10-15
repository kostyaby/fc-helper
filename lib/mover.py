from . import Constant

import os


class Mover:
  def __init__(self, database, clock):
    self.database = database
    self.clock = clock


  def move(self, tracked_directory, unsorted_tracked_entities):
    for tracked_entity in unsorted_tracked_entities:
      if self.clock.delta(tracked_entity.updated_at) <= Constant.Clock.UNSORTED_TO_SORTED_THRESHOLD_MILLIS:
        continue

      directory_a_day_path = self.clock.get_directory_a_day_path(tracked_directory)
      
      if tracked_directory.validate_directory_a_day(directory_a_day_path):
        old_related_path = tracked_entity.related_path
        new_related_path = os.path.join(directory_a_day_path, tracked_entity.related_path)

        os.rename(os.path.join(tracked_directory.path, old_related_path),\
                  os.path.join(tracked_directory.path, new_related_path))

        tracked_entity.related_path = new_related_path
        tracked_entity.status = Constant.TrackedEntity.IGNORED_OR_MISSED
        self.database.update_tracked_entity(tracked_entity)
