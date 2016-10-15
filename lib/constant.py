class Constant:
  class Clock:
    DIRECTORY_A_DAY_TEMPLATE = "Directory-%04d-%02d-%02d"   
    MILLIS_IN_SECOND = 1000
    UNSORTED_TO_SORTED_THRESHOLD_MILLIS = 600000 # 10 minutes


  class Config:
    TRACKED_DIRECTORIES_KEY = "tracked_directories"
    PATH_KEY = "path"
    IGNORE_REGEXES_KEY = "ignore_regexes"

    DIRECTORY_A_DAY_REGEX = "^Directory-[0-9]{4}-[0-9]{2}-[0-9]{2}$"  


  class Database:
    TABLE_PRESENCE_QUERY_TEMPLATE = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"

    TRACKED_ENTITY_TABLE_NAME = "TrackedEntity"

    TRACKED_ENTITY_ID_COLUMN = "Id"
    TRACKED_ENTITY_TRACKED_DIRECTORY_PATH_COLUMN = "TrackedDirectoryPath"
    TRACKED_ENTITY_RELATED_PATH_COLUMN = "RelatedPath"
    TRACKED_ENTITY_STATUS_COLUMN = "Status"
    TRACKED_ENTITY_CREATED_AT_COLUMN = "CreatedAt"
    TRACKED_ENTITY_UPDATED_AT_COLUMN = "UpdatedAt"

    CREATE_TRACKED_ENTITY_TABLE_QUERY = '''CREATE TABLE `{}` (
                                           `Id`  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                                           `TrackedDirectoryPath` TEXT NOT NULL,
                                           `RelatedPath` TEXT NOT NULL,
                                           `Status` INTEGER NOT NULL,
                                           `CreatedAt` INTEGER NOT NULL,
                                           `UpdatedAt` INTEGER NOT NULL)'''.format(TRACKED_ENTITY_TABLE_NAME) 
    SELECT_ALL_TRACKED_ENTITY_QUERY = "SELECT * FROM {}".format(TRACKED_ENTITY_TABLE_NAME)                                       
    INSERT_TRACKED_ENTITY_QUERY_TEMPLATE = "INSERT INTO {} ({}, {}, {}, {}, {}) VALUES (?, ?, ?, ?, ?)".format(\
        TRACKED_ENTITY_TABLE_NAME, TRACKED_ENTITY_TRACKED_DIRECTORY_PATH_COLUMN, TRACKED_ENTITY_RELATED_PATH_COLUMN,\
        TRACKED_ENTITY_STATUS_COLUMN, TRACKED_ENTITY_CREATED_AT_COLUMN, TRACKED_ENTITY_UPDATED_AT_COLUMN)
    UPDATE_TRACKED_ENTITY_QUERY_TEMPLATE = "UPDATE {} SET {}=?, {}=?, {}=?, {}=?, {}=? WHERE {}=?".format(\
        TRACKED_ENTITY_TABLE_NAME, TRACKED_ENTITY_TRACKED_DIRECTORY_PATH_COLUMN, TRACKED_ENTITY_RELATED_PATH_COLUMN,\
        TRACKED_ENTITY_STATUS_COLUMN, TRACKED_ENTITY_CREATED_AT_COLUMN, TRACKED_ENTITY_UPDATED_AT_COLUMN,\
        TRACKED_ENTITY_ID_COLUMN)

                                
  class System:
    APPLICATION_SUPPORT_DIRECTORY = "~/Library/Application Support/FolderControlder"
    CONFIG_FILE = "config.json"
    DATABASE_FILE = "fc.db"                                                                                                       


  class TrackedEntity:
    UNSORTED = 1
    IGNORED_OR_MISSED = 2