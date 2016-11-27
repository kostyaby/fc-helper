from . import Constant


class Blender:
  def __init__(self, database):
    self.database = database


  def blend(self, tracked_directory, crawled_tracked_entities):
    stored_tracked_entities = self.database.fetch_tracked_entities_for(tracked_directory)
    unsorted_tracked_entities = []

    for id, tracked_entity in stored_tracked_entities.iteritems():
      if id not in crawled_tracked_entities:
        self.database.delete_tracked_entity(tracked_entity)
      else:
        unsorted_tracked_entities.append(tracked_entity)

    for tracked_entity in crawled_tracked_entities.iterkeys():
      if tracked_entity not in stored_tracked_entities:
        tracked_directory_path, related_path = tracked_entity
        unsorted_tracked_entities.append(self.database.create_tracked_entity(tracked_directory_path, related_path))

    return unsorted_tracked_entities
