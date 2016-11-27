from . import Constant

import os


class TrackedEntity:
  def __init__(self, id, tracked_directory_path, related_path, created_at):
    self.id = id
    self.tracked_directory_path = tracked_directory_path
    self.related_path = related_path
    self.created_at = created_at


  def get_absolute_path(self):
    return os.path.join(self.tracked_directory_path, self.related_path)


  def __str__(self):
    return "id: {}; tracked_directory_path: {}; related_path: {}; created_at: {}".format(\
        self.id, self.tracked_directory_path, self.related_path, self.created_at)
