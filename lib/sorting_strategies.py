from . import Constant


class SortingStrategyFactory:
  @staticmethod
  def create(sorting_strategy_name, clock):
    if sorting_strategy_name == "directory_a_day":
      return DirectoryADayStrategy(clock)
    else:
      print "Sorting strategy factory failed to create a sorting strategy"
      return None


class AbstractSortingStrategy(object):
  def __init__(self, clock):
    self.clock = clock


  def should_be_skipped(self, tracked_entity):
    livetime_threshold = Constant.SortingStrategies.DirectoryADayStrategy.LIVETIME_THRESHOLD_MILLIS
    return self.clock.delta(tracked_entity.updated_at) <= livetime_threshold


  def avoid_naming_collisions(self, directory_name):
    return "{}-{}".format(directory_name, self.clock.cached_time)


class DirectoryADayStrategy(AbstractSortingStrategy):
  def __init__(self, clock):
    super(DirectoryADayStrategy, self).__init__(clock)


  def get_target_directory_path(self):
    clock = self.clock
    return Constant.SortingStrategies.DirectoryADayStrategy.TEMPLATE % (\
        clock.cached_today.year, clock.cached_today.month, clock.cached_today.day)


  def get_regexes_to_ignore(self):
    return [Constant.SortingStrategies.DirectoryADayStrategy.REGEX]
