esytoobot
=========

This is a bot that will play the RTS game [StarCraft 2](https://starcraft2.com/en-us/).

Usage
-------

You will need the following dependencies

* Python3
* virtualenv
* [Starcraft2 binaries](https://github.com/Blizzard/s2client-proto#downloads)
* [Starcraft2 maps](https://github.com/Blizzard/s2client-proto#map-packs)

> **Protip:** for linux, make sure you unpack the Starcraft 2 folder in you home directory, and rename `Maps` to `maps`

```shell
git clone https://github.com/MrRacoon/esytoobot.git
cd esytoobot
make        # Will enable the virtualenv and install the dependencies
make start  # Starts SC2 and plays the bot
```
