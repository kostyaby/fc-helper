from . import Constants

import sqlite3
import os.path

class Database:
  @staticmethod
  def create_default():
    return Database(os.path.join(os.path.expanduser(Constants.APP_SUPPORT_FOLDER), Constants.DATABASE_FILE))

  def __init__(self, database_path):
    self.connection = sqlite3.connect(database_path)

  def close(self):
    self.connection.close()
