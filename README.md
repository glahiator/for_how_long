# Youtube channel all video duration counter Telegram Bot
**A Telegram bot counts the duration of all videos from the received channel*
- Find it on Telegram as [For How Lone](https://t.me/for_how_long_bot)

## Features
- [X] Using youtube data API.
- [X] Receive video sended by users and count all videos uploaded on the channel.
- [X] Send to user all time duration divided into days hours minutes.
- [X] Save requested data to cache for fast answer if not new videos uploaded.

## ToDo 
- [ ] Handle more exceptions.
- [ ] LOGGER support.
- [ ] Update command.
- [ ] Send channel banner.
- [ ] Set inline bot.

### Installation
- Clone this git repository.
```sh 
git clone https://github.com/glahiator/for_how_long.git
```
- Change Directory
```sh 
cd for_how_long
```
- Install requirements with pip3
```sh 
pip3 install -r requirements.txt
```

### Configuration
**There are way for configuring this bot.**
1. Create file info.ini.
2. Add youtube API key in file with next structure ['API']['KEY'].
3. Add telegram token with next ['TELEGRAM']['TOKEN'].

### Configuration Values
- `config['TELEGRAM']['TOKEN']` - Get it by contacting to [BotFather](https://t.me/botfather)
- `config['API']['KEY']` - Get it by step-by-step complete [guide](https://developers.google.com/youtube/v3/getting-started)

## Copyright & License
- Copyright (©) 2022 by [glahiator](https://github.com/glahiator)
- Licensed under the terms of the [GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007](./LICENSE)
