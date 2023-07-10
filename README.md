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

NOTE: This code was tested on Linux. Adaptations might be required for running on other OS.

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