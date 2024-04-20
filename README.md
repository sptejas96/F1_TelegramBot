# F1 Telegram Bot

## Introduction
This is a telgram bot that can be added to a telegram group and supports the following simple function
- Next Race details
- Driver Standings
- Constructors Standings

## Pre-requisite
- Need a bot token from _Telegram bot father_ [BotFather](https://core.telegram.org/bots/features#botfather)
- python version 3.9+
- python pip

## Installation
1. Clone Git Repository
```sh
git clone https://github.com/sptejas96/F1_TelegramBot.git
```
2. navigate to cloned repository 
```sh
cd F1_TelegramBot
```
3. Add the bot token obtained in "telegram_bot_token.json" file
```json
{
    "token":"<Enter bot token within double quotes>"
}
```
### Standalone on Host OS
4. Install dependencies using pip (Recommended to use python virtual environment to avoid issues with libraries of different versions)
```sh
python3 -m pip install -r requirements.txt
```
5. Run the bot 
```sh
python3 f1telegrambot.py
```
or run it as a background service using nohup (part of linux coreutils package)
```sh
nohup python3 f1telegrambot.py >/dev/null 2>&1 &
```
NOTE: In case of nohup, note down the PID to kill it later to stop the program

### As a Podman or Docker Container
4. Build the image
```
podman build -t f1bot .
```
This will build the image as per the Container file present.
This currently has a Red Hat UBI 9 Minimal Image and installs additional Python dependencies

5. Run the image in a container
```
podman -d run f1bot
```
This runs the container in detached mode.
Use ```podman ps``` to view all running containers.
Use ```podman stop <Container_ID>``` to stop the container

NOTE: Replace 'podman' with 'docker' in above commands if you are using docker.

NOTE: This code was developed and tested on RHEL9. Adaptations might be required for running on other OS.

Refer RHEL guidelines on UBI images here: [access.redhat.com](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html-single/building_running_and_managing_containers/index#con_understanding-the-ubi-standard-images_assembly_types-of-container-images)

## Usage
1. Invite the telegram bot to the telegram group using the name assigned by Telegram BotFather
2. Send the commands and wait for the bot to respond
* ```/nextrace@<BotHandle>```
* ```/drivers@<BotHandle>```
* ```/teams@<BotHandle>```

## Contributors
[Rohan](https://github.com/rohandesai-028)

## LICENSE
MIT

Schedule from: [F1 Schedule](https://github.com/sportstimes/f1/tree/main/_db/f1)