from . import Constant

from datetime import date
import os.path
import time


class Clock:
  def __init__(self):
    self.cached_today = date.today()
    self.cached_time = int(time.time() * Constant.Clock.MILLIS_IN_SECOND)


  def get_directory_a_day_path(self, tracked_directory):
    return Constant.Clock.DIRECTORY_A_DAY_TEMPLATE % (\
        self.cached_today.year, self.cached_today.month, self.cached_today.day)


  def get_timestamped_directory_name(self, dirname):
    return "{}-{}".format(dirname, self.cached_time)

  def delta(self, timestamp):
    return self.cached_time - timestamp
