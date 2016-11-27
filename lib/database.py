from . import Constant
from . import TrackedEntity

from datetime import datetime
import time
import sqlite3
import os.path


class Database:
  @staticmethod
  def create_default(clock):
    return Database(os.path.join(os.path.expanduser(Constant.System.APPLICATION_SUPPORT_DIRECTORY),\
                                                    Constant.System.DATABASE_FILE), clock)


  @staticmethod
  def map_row_to_tracked_entity(row):
    if row is None:
      return None

    return TrackedEntity(row[0], row[1], row[2], row[3])


  @staticmethod
  def tracked_entities_list_to_dictionary(tracked_entities):
    dictionary = {}
    for tracked_entity in tracked_entities:
      dictionary[(tracked_entity.tracked_directory_path, tracked_entity.related_path)] = tracked_entity

    return dictionary


  def __init__(self, database_path, clock):
    self.connection = sqlite3.connect(database_path)
    self.clock = clock

    self.check_and_create_table(Constant.Database.TRACKED_ENTITY_TABLE_NAME,\
                                Constant.Database.CREATE_TRACKED_ENTITY_TABLE_QUERY)


  def check_and_create_table(self, table_name, create_table_query):
    if not self.check_table_presence(table_name):
      self.create_table(create_table_query)


  def check_table_presence(self, table_name):
    cursor = self.connection.cursor()
    cursor.execute(Constant.Database.TABLE_PRESENCE_QUERY_TEMPLATE, [table_name])
    return cursor.fetchone() is not None


  def create_table(self, create_table_query):
    self.connection.execute(create_table_query)


  def fetch_tracked_entities_for(self, tracked_directory):
    cursor = self.connection.cursor()
    cursor.execute(Constant.Database.SELECT_TRACKED_ENTITY_FOR_TRACKED_DIRECTORY_QUERY, [tracked_directory.path])
    return Database.tracked_entities_list_to_dictionary(map(Database.map_row_to_tracked_entity, cursor.fetchall()))


  def create_tracked_entity(self, tracked_directory_path, related_path):
    created_at = self.clock.cached_time

    cursor = self.connection.cursor()
    cursor.execute(Constant.Database.INSERT_TRACKED_ENTITY_QUERY_TEMPLATE,\
      [tracked_directory_path, related_path, created_at])
    self.connection.commit()

    return TrackedEntity(cursor.lastrowid, tracked_directory_path, related_path, created_at)


  def delete_tracked_entity(self, tracked_entity):
    cursor = self.connection.cursor()
    cursor.execute(Constant.Database.DELETE_TRACKED_ENTITY_QUERY_TEMPLATE, [tracked_entity.id])
    self.connection.commit()


  def close(self):
    self.connection.close()
