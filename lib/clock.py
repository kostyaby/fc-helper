from . import Constant

from datetime import date
import os.path
import time


class Clock:
  def __init__(self):
    self.cached_today = date.today()
    self.cached_time = int(time.time() * Constant.Clock.MILLIS_IN_SECOND)


  def get_timestamped_directory_name(self, dirname):
    return "{}-{}".format(dirname, self.cached_time)


  def delta(self, timestamp):
    return self.cached_time - timestamp
