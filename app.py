#!/usr/bin/python

from lib import *

import json


def main():
  clock = Clock()
  database = Database.create_default(clock)
  config = Config.create_default()
  blender = Blender(database, clock)
  mover = Mover(database, clock)

  for tracked_directory in config.get_tracked_directories():
    if not tracked_directory.is_directory():
      print "Tracked directory {} is not a directory!".format(tracked_directory.path)
      continue

    crawled_tracked_entities = tracked_directory.crawl_directory()
    unsorted_tracked_entities = blender.blend(tracked_directory, crawled_tracked_entities)
    mover.move(tracked_directory, unsorted_tracked_entities)

  database.close()


if __name__ == "__main__":
  main()
else:
  print "fc-helper/app.py script is an entrypoint and is supposed to be invoked directly!"
