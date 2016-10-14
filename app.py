#!/usr/bin/python

from lib import *

import json

def main():
  database = Database.create_default()
  config = Config.create_default()

  for tracked_directory in config.get_tracked_directories():
    DirectoryProcessor.create(tracked_directory, database).process()

  database.close()

if __name__ == "__main__":
  main()
else:
  print "fc-helper/app.py script is an entrypoint and is supposed to be invoked directly!"
