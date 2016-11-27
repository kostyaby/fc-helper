class Constant:
  class Clock:
    MILLIS_IN_SECOND = 1000

  class Config:
    IGNORE_REGEXES_KEY = "ignore_regexes"
    PATH_KEY = "path"
    SORTING_STRATEGY_KEY = "sorting_strategy"
    TRACKED_DIRECTORIES_KEY = "tracked_directories"


  class Database:
    TABLE_PRESENCE_QUERY_TEMPLATE = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"

    TRACKED_ENTITY_TABLE_NAME = "TrackedEntity"

    TRACKED_ENTITY_ID_COLUMN = "Id"
    TRACKED_ENTITY_TRACKED_DIRECTORY_PATH_COLUMN = "TrackedDirectoryPath"
    TRACKED_ENTITY_RELATED_PATH_COLUMN = "RelatedPath"
    TRACKED_ENTITY_CREATED_AT_COLUMN = "CreatedAt"

    CREATE_TRACKED_ENTITY_TABLE_QUERY = '''CREATE TABLE `{}` (
                                           `Id`  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                                           `TrackedDirectoryPath` TEXT NOT NULL,
                                           `RelatedPath` TEXT NOT NULL,
                                           `CreatedAt` INTEGER NOT NULL)'''.format(TRACKED_ENTITY_TABLE_NAME)
    SELECT_TRACKED_ENTITY_FOR_TRACKED_DIRECTORY_QUERY = "SELECT * FROM {} WHERE TrackedDirectoryPath=?".format(\
        TRACKED_ENTITY_TABLE_NAME)
    INSERT_TRACKED_ENTITY_QUERY_TEMPLATE = "INSERT INTO {} ({}, {}, {}) VALUES (?, ?, ?)".format(\
        TRACKED_ENTITY_TABLE_NAME, TRACKED_ENTITY_TRACKED_DIRECTORY_PATH_COLUMN,\
        TRACKED_ENTITY_RELATED_PATH_COLUMN, TRACKED_ENTITY_CREATED_AT_COLUMN)
    DELETE_TRACKED_ENTITY_QUERY_TEMPLATE = "DELETE FROM {} WHERE {}=?".format(\
        TRACKED_ENTITY_TABLE_NAME, TRACKED_ENTITY_ID_COLUMN)


  class SortingStrategies:
    class DirectoryADayStrategy:
      TEMPLATE = "Directory-%04d-%02d-%02d"
      REGEX = "^Directory-[0-9]{4}-[0-9]{2}-[0-9]{2}$"
      LIVETIME_THRESHOLD_MILLIS = 600000 # = 10 minutes


    class SmartCategoryStrategy:
      MOVIES = "Folder-Movies"
      MUSIC = "Folder-Music"
      PICTURES = "Folder-Pictures"
      DOCUMENTS = "Folder-Documents"
      OTHER = "Folder-Other"

      EXTENSION_REGEX = "([^\s]+(\.(?i)({}))$)"

      MOVIES_EXTENSIONS = ["avi", "mov", "vob", "m4v", "mp4"]
      MUSIC_EXTENSIONS = ["mp3", "flac", "m4a", "aac", "wav"]
      PICTURES_EXTENSIONS = ["jpg", "png", "gif", "bmp"]
      DOCUMENTS_EXTENSIONS = ["doc", "pdf"]

      DOMINANT_CATEGORY_FACTOR = 0.8

      REGEX = "^({})|({})|({})|({})|({})$".format(MOVIES, MUSIC, PICTURES, DOCUMENTS, OTHER)
      LIVETIME_THRESHOLD_MILLIS = 86400000 # = 24 hours

                                
  class System:
    APPLICATION_SUPPORT_DIRECTORY = "~/Library/Application Support/FolderControlder"
    CONFIG_FILE = "config.json"
    DATABASE_FILE = "fc.db"                                                                                                       
