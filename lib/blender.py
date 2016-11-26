from . import Constant


class Blender:
  def __init__(self, database):
    self.database = database


  def blend(self, tracked_directory, crawled_tracked_entities):
    stored_tracked_entities = self.database.fetch_all_tracked_entities()
    unsorted_tracked_entities = []

    for id, tracked_entity in stored_tracked_entities.iteritems():
      if id not in crawled_tracked_entities:
        tracked_entity.status = Constant.TrackedEntity.IGNORED_OR_MISSED
        self.database.update_tracked_entity(tracked_entity)
      else:
        if tracked_entity.status == Constant.TrackedEntity.IGNORED_OR_MISSED:
          tracked_entity.status = Constant.TrackedEntity.UNSORTED
          self.database.update_tracked_entity(tracked_entity)
        unsorted_tracked_entities.append(tracked_entity)

    for crawled_tracked_entity in crawled_tracked_entities.iterkeys():
      if crawled_tracked_entity not in stored_tracked_entities:
        tracked_directory_path, related_path = crawled_tracked_entity
        unsorted_tracked_entities.append(self.database.create_tracked_entity(tracked_directory_path, related_path))

    return unsorted_tracked_entities


    


