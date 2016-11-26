from . import Constant
from . import TrackedDirectory

import json
import os.path


class Config:
  @staticmethod
  def create_default(clock):
    return Config(os.path.join(os.path.expanduser(Constant.System.APPLICATION_SUPPORT_DIRECTORY),\
                                                  Constant.System.CONFIG_FILE), clock)


  def __init__(self, config_path, clock):
    with open(config_path, "r") as config_file:
      self.tracked_directories = \
          [TrackedDirectory(data, clock) for data in json.load(config_file)[Constant.Config.TRACKED_DIRECTORIES_KEY]]


  def get_tracked_directories(self):
    return self.tracked_directories
