esytoobot
=========

This is a bot that will play the RTS game [StarCraft 2](https://starcraft2.com/en-us/).

This bot is primarily developed in ubuntu. I can help you get setup on ubuntu, but you're on your own for windows/macos.

Usage
-------

You will need the following dependencies

* Python3
* [virtualenv](https://virtualenv.pypa.io/en/latest/)
* [Starcraft2 binaries](https://github.com/Blizzard/s2client-proto#downloads)
* [Starcraft2 maps](https://github.com/Blizzard/s2client-proto#map-packs)

> **Protip:** for linux, make sure you unpack the Starcraft 2 folder in you home directory, and rename `Maps` to `maps`

```shell
git clone https://github.com/MrRacoon/esytoobot.git
cd esytoobot
make        # Will enable the virtualenv and install the dependencies
make start  # Starts SC2 and plays the bot
```


Profiling
---------

```
pip install snakeviz
then in python
import os

os.system("py -3.7 -m cProfile -o run.prof run.py")
os.system("snakeviz run.prof")

after the game closes or you close it, your browser should display the profile results
read more about snakeviz here https://jiffyclub.github.io/snakeviz/(edited)
SnakeViz
SnakeViz is a browser based graphical viewer for the output of Python's cProfile module.
```