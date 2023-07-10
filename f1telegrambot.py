#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""
Basic example for a bot that works with polls. Only 3 people are allowed to interact with each
poll/quiz the bot generates. The preview command generates a closed poll/quiz, exactly like the
one the user sends the bot
"""

""" Import Python packages"""
import datetime
import pytz
import logging
import pandas as pd
from telegram import __version__ as TG_VER
from bs4 import BeautifulSoup
import requests
import tabulate
import numpy as np
import json

"""Version check"""
try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )

"""Import more packages if Version check passes"""
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

"""
Next race function

This function is called from the main when the command nextrace is sent from telegram.
This provides details of the next race in F1 Calendar
"""
async def next_race(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    '''respond with upcoming race details'''
    race_list = pd.read_csv('poll_data.csv') #poll_data.csv contains details of F1 Races for the year. This needs to be regenerated every year

    #Temporary rows to extract Race Month and Day to compare with current Month and Day 
    race_list['race_month'] = race_list["sessions/fp1"].str.slice(5,7)
    race_list['race_month'] = race_list['race_month'].astype(int)
    race_list['race_day'] = race_list["sessions/fp1"].str.slice(8,10)
    race_list['race_day'] = race_list['race_day'].astype(int)
    race_list['curr_day'] = datetime.date.today().day
    race_list['curr_month'] = datetime.date.today().month

    #All Magic happens in the below few lines
    next_race = race_list.query('race_month == curr_month & race_day > curr_day')
    if next_race.empty:
        #This is to handle the Dry Race season T_T
        race_list['curr_month'] = datetime.date.today().month + 1
        next_race = race_list.query('race_month == curr_month')
    
    #Extract details to publish
    race_name = next_race["name"].values[0]
    race_location = next_race["location"].values[0]
    quali_date = next_race["sessions/qualifying"].values[0]
    gp_date = next_race["sessions/gp"].values[0]
    
    #Converting to IST (GMT+5:30)
    quali_IST=convert_time(quali_date)
    gp_IST=convert_time(gp_date)
    fmt = '%Y-%m-%d %H:%M:%S %Z%z'
    
    #Create a reply message to user command
    await update.message.reply_text(f'Name: {race_name}\nLocation: {race_location} \nQualifying: {quali_IST.strftime(fmt)} \nGrand Prix: {gp_IST.strftime(fmt)}')

"""
Convert Time helper function

This function is called from the next race call when the command nextrace is sent from telegram.
This converts the date time given in 2023-03-03T11:30:00Z format in UST to IST
"""
def convert_time(UTC_Time):
    #Extract Date and Time parameters
    yyyy =int(UTC_Time[0:4])
    mm = int(UTC_Time[5:7])
    dd = int(UTC_Time[8:10])
    hr = int(UTC_Time[11:13])
    mins = int(UTC_Time[14:16])
    
    #Create a python datetime object
    UTC_obj = datetime.datetime(yyyy, mm, dd, hr, mins)
    
    #Convert from UST to IST
    tz = pytz.timezone('Asia/Calcutta') # Change as per your Time Zone https://pypi.org/project/pytz/
    IST_Obj = UTC_obj.replace(tzinfo=pytz.utc).astimezone(tz)
    return IST_Obj


"""
Drivers function

This function is called from the main when the command drivers is sent from telegram.
This provides details on the Driver standings in the form of a table.
This function scrapes the data from the official F1 Website and processes it
Currently tested for year 2023 and might need update if Webpage gets updated
"""
async def drivers(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Step 1: Preparing the Soup - Yummy Data!!
    source = requests.get("https://www.formula1.com/en/results.html/2023/drivers.html").text
    soup = BeautifulSoup(source, 'lxml')
    
    # Step 2:  Search for required flavours in the Soup
    first_names = soup.find_all('span', class_='hide-for-tablet')
    points = soup.find_all('td', class_="dark bold")
    
    # Step 3: Pack it as a Table
    field_names = ["DRIVER", "POINTS"]
    col1 = []
    col2 = []
    for i in range(len(first_names)):
        col1.append(first_names[i].string)
        col2.append(points[i].string)
    points_table = np.transpose(np.array([col1, col2]))
    pt_table = tabulate.tabulate(points_table, field_names)

    # Create a reply message to user command
    await update.message.reply_text(f'<pre>{pt_table}</pre>', parse_mode=ParseMode.HTML)

"""
Teams function

This function is called from the main when the command teams is sent from telegram.
This provides details on the Constructor standings in the form of a table.
This function scrapes the data from the official F1 Website and processes it
Currently tested for year 2023 and might need update if Webpage gets updated
"""
async def teams(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Step 1: Preparing the Soup - Yummy Data!!
    source = requests.get("https://www.formula1.com/en/results.html/2023/team.html").text
    soup = BeautifulSoup(source, 'lxml')

    # Step 2:  Search for required flavours in the Soup
    team_name = soup.find_all('a', class_="dark bold uppercase ArchiveLink")
    points = soup.find_all('td', class_="dark bold")
    
    # Step 3: Pack it as a Table
    field_names = ["TEAM", "POINTS"]
    col1 = []
    col2 = []
    for i in range(len(team_name)):
        col1.append(team_name[i].string)
        col2.append(points[i].string)
    points_table = np.transpose(np.array([col1, col2]))
    pt_table = tabulate.tabulate(points_table, field_names)
    
    # Create a reply message to user command
    await update.message.reply_text(f'<pre>{pt_table}</pre>', parse_mode=ParseMode.HTML)

"""
get_token()

Helper function to get token from telegram_bot_token.json file in root directory
"""
def get_token():
    f = open ('telegram_bot_token.json', "r")
    token = json.loads(f.read())
    f.close()
    return (token["token"])

"""
Main function

Here is where everything happens!!
"""
def main() -> None:
    """Run bot."""
    # Create the Application and pass it your bot's token.
    bot_token = f"{get_token()}"
    application = Application.builder().token(bot_token).build()

    # Add the BOT Commands
    application.add_handler(CommandHandler("nextrace", next_race))
    application.add_handler(CommandHandler("drivers", drivers))
    application.add_handler(CommandHandler("teams", teams))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()

# END OF FILE | Do Not Type Anything Below This Line