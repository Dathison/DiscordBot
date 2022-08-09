import subprocess
import secrets
import discord
#import table
import laliga_table
import cl_table
import spurs_fixtures
import lxml
import requests
from bs4 import BeautifulSoup
import re
import time
import asyncio
from tabulate import tabulate
#import pandas as pd
from discord.ext import commands

TOKEN = secrets.discord_token

description = '''Piss Bot for the Piss people!'''
bot = commands.Bot(command_prefix='!', description=description)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def piss(ctx):
    """Says world"""
    await ctx.send("Hello world!")

@bot.command()
async def laliga_table(ctx):

    "Shows the La Liga table of the current season."

    def ll_table():
        lal_table_link = f"https://onefootball.com/en/competition/laliga-10/table"
        lal_table_source = requests.get(lal_table_link).text
        lal_table_page = BeautifulSoup(lal_table_source, "lxml")
        lal_tab = lal_table_page.find_all("a", class_="standings__row-grid")

        lal_table = []
        lal_table.append("  ________________ PL W D L GD PTS")

        for i in range(len(lal_tab)):
            lal_tab[i].insert('1', 'test')
            lal_table.append(lal_tab[i].text.strip())

        ll_tab = '\n'.join(lal_table) # Converts the single-line list into a line-separated list.
        return ll_tab # Defining the output of premierleague_table sent to whatever function uses it.

    await ctx.send(ll_table())

@bot.command()
async def pl_table(ctx):

    def pl_table():
        prem_table_link = f"https://onefootball.com/en/competition/premier-league-9/table"
        prem_table_source = requests.get(prem_table_link).text
        prem_table_page = BeautifulSoup(prem_table_source, "lxml")
#        prem_tab = prem_table_page.find_all("a", class_="standings__row-grid")
        teams_prem_table = prem_table_page.find_all("p", class_="title-7-medium standings__team-name")
        points_prem_table = prem_table_page.find_all("span", class_="title-7-bold")
        stats_prem_table = prem_table_page.find_all("span", class_="standings__cell-text--dimmed")

        ### TESTING AREA ###
        ### Prints alphabetical list of all Premier League teams ###

        temp_teams_table = []  # Empty table created to be filled later.
        temp_points_table = []
        temp_stats_table = []
        numbers_table = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20']  # List of numbers manually inputted. Will later be changed and have the script automatically fetch these from the site.
        headers = ["Pos","Team", "GP", "W", "D", "L", "GD", "Pts"]


        for i in range(len(teams_prem_table)):  # For every line temp_tab:
            temp_teams_table.append(teams_prem_table[i].text.strip())  # Add a line to temp_table and strip away the formatting.

        for i in range(len(points_prem_table)):
            temp_points_table.append(points_prem_table[i].text.strip())

        for i in range(len(stats_prem_table)):
            temp_stats_table.append(stats_prem_table[i].text.strip())



        intermediate_prem_table = zip(numbers_table, temp_teams_table, temp_stats_table[0::5], temp_stats_table[1::5], temp_stats_table[2::5], temp_stats_table[3::5], temp_stats_table[4::5], temp_points_table[1::2])  # Add the two tables together, row for row. The temp_points_table only selected every second entry of the table starting from the first uneven numbers. This is due to how the website is formatted.

        final_prem_table = tabulate(intermediate_prem_table, headers=headers)

        print(final_prem_table)
        return final_prem_table
#        for entry in final_prem_table:  # For every entry in final_prem_table:
#            print(entry[0], entry[1])  # Print the first column first, then the second.

#        print(list(final_prem_table))

        ### Prints a full table of the Premier League and posts it in response to the user sending the command ###


        prem_table = []
        prem_table.append("  ________________ PL W D L GD PTS")

        for i in range(len(prem_tab)):

            if 'Arsenal' in prem_tab[i].text:
                prem_tab[i].append(" <----- Wow these guys are shit!")

            prem_table.append(prem_tab[i].text.strip())

        b = '\n'.join(prem_table)
#        return b
        
    await ctx.send(f'``` {pl_table()} ```')

@bot.command()
async def cl_table(ctx):

    "Shows the Champions League table of the current season."
    cl_table()
    cl_table_output = open("cl_table_output","r")
    await ctx.send(f"``` {cl_table_output.read()} ```")

@bot.command()
async def shutdown(self,ctx):
    if ctx.message.author.id == 150634514035507200: #replace OWNERID with your user id
      print("shutdown")
      try:
        await self.bot.logout()
      except:
        print("EnvironmentError")
        self.bot.clear()
    else:
      await ctx.send("You do not own this bot!")

@bot.command()
async def fixtures(ctx):
    fixtures_link = f"https://onefootball.com/en/competition/premier-league-9/fixtures"
    fixtures_source = requests.get(fixtures_link).text
    fixtures_page = BeautifulSoup(fixtures_source, "lxml")
    fix = fixtures_page.find_all("li", class_="simple-match-cards-list__match-card")

    def fixtures_list():
        fixtures = []
        for i in range(len(fix)):
            fixtures.append(fix[i].text.strip())

        return fixtures

    def get_fixtures(team):
        fixtures = fixtures_list()
        a = []
        for i in range(len(fixtures)):
            if team in fixtures[i]:
                a.append(fixtures[i])
        a = '\n'.join(a)
        return a

    "Shows the fixture schedule of the current month for Spurs."
    # spurs_fixtures
    # spurs_fixtures_output = open("spurs_fixtures_output","r")
    # await ctx.send(spurs_fixtures_output.read())
    await ctx.send(str(get_fixtures("Tottenham")))

@bot.command()
async def pisstest(ctx):
    await ctx.send(f"This is a test string. Please type ''a'' or ''b''")

#    def check(msg):
# 	        msg.content.lower() in ["a", "b"]

    msg = await bot.wait_for("message", timeout=30)
    if msg.content() == "a" or msg.content() == "b":
        await ctx.send("Success!")
    else:
        await ctx.send("Failed!")

bot.run(TOKEN)
