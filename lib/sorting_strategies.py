from . import Constant

import os
import re


class SortingStrategyFactory:
  @staticmethod
  def create(sorting_strategy_name, clock):
    if sorting_strategy_name == "directory_a_day":
      return DirectoryADayStrategy(clock)
    elif sorting_strategy_name == "smart_category":
      return SmartCategoryStrategy(clock)
    else:
      print "Sorting strategy factory failed to create a sorting strategy"
      return None


class AbstractSortingStrategy(object):
  def __init__(self, clock):
    self.clock = clock


  def avoid_naming_collisions(self, directory_name):
    return "{}-{}".format(directory_name, self.clock.cached_time)


class DirectoryADayStrategy(AbstractSortingStrategy):
  def __init__(self, clock):
    super(DirectoryADayStrategy, self).__init__(clock)


  def get_target_directory_path(self, tracked_entity):
    clock = self.clock
    return Constant.SortingStrategies.DirectoryADayStrategy.TEMPLATE % (\
        clock.cached_today.year, clock.cached_today.month, clock.cached_today.day)


  def get_regexes_to_ignore(self):
    return [Constant.SortingStrategies.DirectoryADayStrategy.REGEX]


  def should_be_skipped(self, tracked_entity):
    livetime_threshold = Constant.SortingStrategies.DirectoryADayStrategy.LIVETIME_THRESHOLD_MILLIS
    return self.clock.delta(tracked_entity.created_at) <= livetime_threshold


class SmartCategoryStrategy(AbstractSortingStrategy):
  def __init__(self, clock):
    super(SmartCategoryStrategy, self).__init__(clock)


  def fill_extension_regex(self, extensions):
    return Constant.SortingStrategies.SmartCategoryStrategy.EXTENSION_REGEX.format("|".join(extensions))


  def get_categories(self):
    return [
        (Constant.SortingStrategies.SmartCategoryStrategy.MOVIES,\
            self.fill_extension_regex(Constant.SortingStrategies.SmartCategoryStrategy.MOVIES_EXTENSIONS)),
        (Constant.SortingStrategies.SmartCategoryStrategy.MUSIC,\
            self.fill_extension_regex(Constant.SortingStrategies.SmartCategoryStrategy.MUSIC_EXTENSIONS)),
        (Constant.SortingStrategies.SmartCategoryStrategy.PICTURES,\
            self.fill_extension_regex(Constant.SortingStrategies.SmartCategoryStrategy.PICTURES_EXTENSIONS)),
        (Constant.SortingStrategies.SmartCategoryStrategy.DOCUMENTS,\
            self.fill_extension_regex(Constant.SortingStrategies.SmartCategoryStrategy.DOCUMENTS_EXTENSIONS))]


  def determine_category(self, file_path, categories):
    for category in categories:
      directory, regex = category
      if re.search(regex, file_path):
        return directory

    return Constant.SortingStrategies.SmartCategoryStrategy.OTHER


  def get_tracked_entity_content_with_categories(self, tracked_entity):
    absolute_path = tracked_entity.get_absolute_path()
    content = []
    categories = self.get_categories()

    if os.path.isfile(absolute_path):
      content.append(absolute_path)
    elif os.path.isdir(absolute_path):
      for (dirpath, dirnames, filenames) in os.walk(absolute_path):
        for filename in filenames:
          absolute_file_path = os.path.join(dirpath, filename)
          content.append(absolute_file_path)

    return [(file_path, os.path.getsize(file_path), self.determine_category(file_path, categories))
        for file_path in content]


  def get_target_directory_path(self, tracked_entity):
    content = self.get_tracked_entity_content_with_categories(tracked_entity)

    category_sizes = {}
    total_size = 0
    for file in content:
      file_size = file[1]
      category = file[2]

      category_sizes[category] = category_sizes.get(category, 0) + file_size
      total_size += file_size

    largest_category_name = Constant.SortingStrategies.SmartCategoryStrategy.OTHER
    largest_category_size = 0
    for key, value in category_sizes.iteritems():
      if largest_category_size < value:
        largest_category_name, largest_category_size = key, value

    if largest_category_size > total_size * Constant.SortingStrategies.SmartCategoryStrategy.DOMINANT_CATEGORY_FACTOR:
      return largest_category_name

    return Constant.SortingStrategies.SmartCategoryStrategy.OTHER


  def get_regexes_to_ignore(self):
    return [Constant.SortingStrategies.SmartCategoryStrategy.REGEX]


  def should_be_skipped(self, tracked_entity):
    livetime_threshold = Constant.SortingStrategies.SmartCategoryStrategy.LIVETIME_THRESHOLD_MILLIS
    return self.clock.delta(tracked_entity.created_at) <= livetime_threshold
