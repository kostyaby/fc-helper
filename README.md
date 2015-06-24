## fc-helper

fc-helper is a command-line tool, which will be used as a part of the FolderControlder application some day. FolderControlder, apparently, is an application that controls folders on your OS X and keeps them clean and organized.

There's no proper instruction how to use fc-helper, but if you really want to try it, then here are some basic tips:

* Make a folder `~/Library/Application Support/FolderControlder` on your Mac
* Put an `info.json` file into that folder(see an example of `info.json`)
* Put an `by.kostya.fc-helper.plist` from this repository into the `~/Library/LaunchAgents` folder
* Change the `Program` key in the .plist file by putting a valid path to the `helper.py` file on your Mac
* Do `launchctl load ~/Library/LaunchAgents/by.kostya.fc-helper.plist` in your Terminal

Hope these tips are helpful!