# AutoMod

Simple overview of use/purpose.

## Description

A discord bot that autobans blacklisted users.

## Getting Started

### Dependencies

* disnake @ git+https://github.com/DisnakeDev/disnake@d6341caa8836239bc672cab7f87254a0ee027e00
* python-3.9.9
* APScheduler==3.8.1

### Installing

* Make sure to go through and add your log channel id inside of the autoban.py file, add your discord token to the token.0 file and then add your guild id inside of the autoban.py file and the __init__.py file inside of the bot folder.

### Executing program

Open cmd prompt and navigate to where the bot folder is store then run this command.
```
python launcher.py
```

### Bot Commands
```
/abl - add an ID to the blacklist
/rbl - remove an ID from the blacklist
```
### Todo
* Add unban feature by using discord ID

## Version History
* 0.2
   * Converted to DB instead of .json file. 
   * Added ability to blacklist names
* 0.1
    * Initial Release

## License

This project is licensed under the GNU License - see the LICENSE.md file for details
