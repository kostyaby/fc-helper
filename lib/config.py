from . import Constants
from . import TrackedDirectory

import json
import os.path

class Config:
  @staticmethod
  def create_default():
    return Config(os.path.join(os.path.expanduser(Constants.APP_SUPPORT_FOLDER), Constants.CONFIG_FILE))

  def __init__(self, config_path):
    with open(config_path, "r") as config_file:
      self.tracked_directories = \
          [TrackedDirectory.create(data) for data in json.load(config_file)[Constants.TRACKED_DIRECTORIES_KEY]]

  def get_tracked_directories(self):
    return self.tracked_directories
