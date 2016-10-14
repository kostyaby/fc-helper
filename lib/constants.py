class Constants:
  APP_SUPPORT_FOLDER = "~/Library/Application Support/FolderControlder"
  
  CONFIG_FILE = "config.json"
  DATABASE_FILE = "fc.db"

  TRACKED_DIRECTORIES_KEY = "tracked_directories"
  PATH_KEY = "path"
  IGNORE_REGEXES_KEY = "ignore_regexes"

  DIRECTORY_A_DAY_TEMPLATE = "Directory-%04d-%02d-%02d"
  DIRECTORY_A_DAY_REGEX = "^Directory-[0-9]{4}-[0-9]{2}-[0-9]{2}$"
