> [!NOTE]
> Readme file is in progress

# VNTU Timetable Bot
This repo contains the source code of [vntu_timetable_bot](t.me/vntu_timetable_bot) - bot that provides timetable of classes by scraping this information from JetIQ presonal cabinet.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)

## Installation
In order to launch docker container you need:

1. Create .env file in /bot directory by given example:  
```
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_PORT=
POSTGRES_HOST=db # docker servise

JETIQ_LOGIN=
JETIQ_AVATAR_ID= # you can find it in source code
JETIQ_PASSWORD=

BOT_TOKEN=
```
1.1 Change admin's id in file /bot/phrases.py to yours id
```
admin_id =
```
2. Run command:
```
make makedir
```
3. Run
```
docker-compose up -d --build
```
4. Create db inside of docker container with your postgres_db name. Make sure bot got connected to it.
5. .....
6. PROFIT!!

(Still in progress so maybe not :trollface:)

## Usage
Here the list of avalible commands for different users:

### Avalible Admin commands:

`/update_timetable` - updates txt files and timetable.

`/update_txt` - updates only txt files by connecting to the JetIQ and reciving latest info.

`/update_data` - updates only database from json files, does not reciving latest info.

`/mailing` - sends given message to every user who pressed /start at least ones.

`/presidents` - list of current presidents.

`/add_president` - adds president (requires user id).

`/remove_president` - removes president (requires user id).

`/users` - sends the amout of users who pressed /start at least ones.

### Avalible president commands:

`/links` - gives option to set or remove links.
