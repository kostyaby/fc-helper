from . import Constant


class TrackedEntity:
  def __init__(self, id, tracked_directory_path, related_path, status, created_at, updated_at):
    self.id = id
    self.tracked_directory_path = tracked_directory_path
    self.related_path = related_path
    self.status = status
    self.created_at = created_at
    self.updated_at = updated_at


  def __str__(self):
    return "id: {}; tracked_directory_path: {}; related_path: {}; status: {}; created_at: {}; updated_at: {}".format(\
      self.id, self.tracked_directory_path, self.related_path, self.status, self.created_at, self.updated_at)
