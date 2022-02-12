# AutoMod

Simple overview of use/purpose.

## Description

A discord bot that autobans blacklisted users. This bot uses a json file to read discord IDs from and bans users based on those IDs. 

## Getting Started

### Dependencies

* disnake @ git+https://github.com/DisnakeDev/disnake@d6341caa8836239bc672cab7f87254a0ee027e00
* python-3.9.9
* APScheduler==3.8.1

### Installing

* Make sure to go through and add your log channel id inside of the autoban.py file, add your discord token to the token.0 file and then add your guild id inside of the autoban.py file and the __init__.py file inside of the bot folder.
* Any modifications needed to be made to files/folders

### Executing program

Open cmd prompt and navigate to where the bot folder is store then run this command.
```
python launcher.py
```

## Version History

* 0.1
    * Initial Release

## License

This project is licensed under the GNU License - see the LICENSE.md file for details
