# Vntu_timetable_bot

> [!NOTE]
> Readme file is in progress

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
2. Run command:
```
make makedir
```
3. Create db with your postgres_db name
4. Run
```
docker-compose up -d
```
5. .....
6. PROFIT!!
(Still in progress so maybe not :trollface:)
