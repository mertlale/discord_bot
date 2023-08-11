# Discord Music Bot

This repository contains the source code and the list of necessary packages for my Discord Music Bot project.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)

[//]: # (- [Usage]&#40;#usage&#41;)

[//]: # (- [Contributing]&#40;#contributing&#41;)

[//]: # (- [License]&#40;#license&#41;)

## Introduction

This repository contains the bot's source file that you can run using the token of the bot you created on the Discord Developer Portal.

## Features

The bot's default prefix is dot. You can write to the message section of your discord channel by adding the prefix (ex: ".play the_song"). 
The bot starts playing the song on your channel by searching the URL or the song name you typed after the play command. When you add songs one after the other, the bot keeps it in a list and continues to play in order.

The commands supported by the bot are as follows:
- `.play <query>`  Plays the song, or adds it to the playlist if a song has already been added. <query> can be the song's URL on youtube or the name of the song.
- `.stop` Stops playing and clears the playlist.
- `.pause`  Pauses the playing song.
- `.resume`  Resumes the song that was paused.
- `.queue`  Lists the songs in the playlist.
- `.skip` Skips to the next song in the playlist

## Installation

A python version that supports packages in the requirements.txt file (ex: python 3.10.12) and pip must be installed before this setup.

Open the terminal of the OS you are using and navigate to the directory of the bot file. Here, install all the packages required for your bot to work by entering the following command:

```shell
pip install -r requirements.txt
```

In the last line in discord_music_bot.py, replace 'your_bot_token' with your own bot's token that you got from Discord Developer Portal:

```python
bot.run('your_bot_token')
```

Then run the discord_music_bot.py. After running the bot and entering the voice channel in discord, you can enter the commands of the bot in any of your message channels. Note: You must have given the necessary permissions to the bot.

[//]: # ()
[//]: # (## Usage)

[//]: # ()
[//]: # (Provide instructions on how to use your project. Include code examples, command-line instructions, or any relevant details.)

[//]: # ()
[//]: # (## Contributing)

[//]: # ()
[//]: # (Indicate how others can contribute to your project. Whether it's through bug reports, feature requests, or pull requests, let people know how they can get involved.)

[//]: # ()
[//]: # (## License)

[//]: # ()
[//]: # (Specify the license under which your project is released. For example, you can use the MIT License, GNU General Public License, or any other open-source license.)


