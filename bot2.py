import subprocess
import secrets
import discord
import cl_table
import spurs_fixtures
import lxml
import requests
from bs4 import BeautifulSoup
import re
import time
import asyncio
from tabulate import tabulate
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
        laliga_table_link = f"https://onefootball.com/en/competition/laliga-10/table"
        laliga_table_source = requests.get(laliga_table_link).text
        laliga_table_page = BeautifulSoup(laliga_table_source, "lxml")
        # pos_prem_table = laliga_table_page.find_all("a", class_="standings__cell standings__cell--numeric")
        teams_laliga_table = laliga_table_page.find_all("p", class_="title-7-medium standings__team-name")
        points_laliga_table = laliga_table_page.find_all("span", class_="title-7-bold")
        stats_laliga_table = laliga_table_page.find_all("span", class_="standings__cell-text--dimmed")

        ### Prints columnised table of the Premier League at the moment of command execution ###

        # temp_pos_table = []
        temp_laliga_teams_table = []  # Empty table created to be filled later.
        temp_laliga_points_table = []
        temp_laliga_stats_table = []
        numbers_table = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17',
                         '18', '19',
                         '20']  # List of numbers manually inputted. Will later be changed and have the script automatically fetch these from the site.
        headers = ["Pos", "Team", "GP", "W", "D", "L", "GD", "Pts"]

        # for i in range (len(pos_prem_table)):
        #    temp_pos_table.append(pos_prem_table[i].text.strip())

        for i in range(len(teams_laliga_table)):  # For every line temp_tab:
            temp_laliga_teams_table.append(
                teams_laliga_table[i].text.strip())  # Add a line to temp_table and strip away the formatting.

        for i in range(len(points_laliga_table)):
            temp_laliga_points_table.append(points_laliga_table[i].text.strip())

        for i in range(len(stats_laliga_table)):
            temp_laliga_stats_table.append(stats_laliga_table[i].text.strip())

        #  stats_prem_table returns GP, W, D, L, and GD all in one go. This is why the following function can simply reuse the variable by starting the table count at different rows.
        intermediate_laliga_table = zip(numbers_table, temp_laliga_teams_table, temp_laliga_stats_table[0::5], temp_laliga_stats_table[1::5],
                                      temp_laliga_stats_table[2::5], temp_laliga_stats_table[3::5], temp_laliga_stats_table[4::5],
                                      temp_laliga_points_table[
                                      1::2])  # Add the two tables together, row for row. The temp_points_table only selected every second entry of the table starting from the first uneven numbers. This is due to how the website is formatted.

        final_laliga_table = tabulate(intermediate_laliga_table, headers=headers)

        print(final_laliga_table)
        return final_laliga_table

    await ctx.send(ll_table())

@bot.command()
async def pl_table(ctx):

    def pl_table():
        prem_table_link = f"https://onefootball.com/en/competition/premier-league-9/table"
        prem_table_source = requests.get(prem_table_link).text
        prem_table_page = BeautifulSoup(prem_table_source, "lxml")
        #pos_prem_table = prem_table_page.find_all("a", class_="standings__cell standings__cell--numeric")
        teams_prem_table = prem_table_page.find_all("p", class_="title-7-medium standings__team-name")
        points_prem_table = prem_table_page.find_all("span", class_="title-7-bold")
        stats_prem_table = prem_table_page.find_all("span", class_="standings__cell-text--dimmed")

        ### Prints columnised table of the Premier League at the moment of command execution ###

        #temp_pos_table = []
        temp_teams_table = []  # Empty table created to be filled later.
        temp_points_table = []
        temp_stats_table = []
        numbers_table = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20']  # List of numbers manually inputted. Will later be changed and have the script automatically fetch these from the site.
        headers = ["Pos","Team", "GP", "W", "D", "L", "GD", "Pts"]


        #for i in range (len(pos_prem_table)):
        #    temp_pos_table.append(pos_prem_table[i].text.strip())

        for i in range(len(teams_prem_table)):  # For every line temp_tab:
            temp_teams_table.append(teams_prem_table[i].text.strip())  # Add a line to temp_table and strip away the formatting.

        for i in range(len(points_prem_table)):
            temp_points_table.append(points_prem_table[i].text.strip())

        for i in range(len(stats_prem_table)):
            temp_stats_table.append(stats_prem_table[i].text.strip())

### DOESN'T WORK ### #  Code for inserting a line at certain lines in the table.
#        numbers_table.insert(4, "---")
#        temp_teams_table.insert(4, " ")
#        temp_stats_table.insert(4, " ")
#        temp_points_table.insert(4, " ")

        #  stats_prem_table returns GP, W, D, L, and GD all in one go. This is why the following function can simply reuse the variable by starting the table count at different rows.
        intermediate_prem_table = zip(numbers_table, temp_teams_table, temp_stats_table[0::5], temp_stats_table[1::5], temp_stats_table[2::5], temp_stats_table[3::5], temp_stats_table[4::5], temp_points_table[1::2])  # Add the two tables together, row for row. The temp_points_table only selected every second entry of the table starting from the first uneven numbers. This is due to how the website is formatted.

        final_prem_table = tabulate(intermediate_prem_table, headers=headers)

        print(final_prem_table)
        return final_prem_table

    await ctx.send(f'``` {pl_table()} ```')

@bot.command()
async def buli_table(ctx):

    "Shows the La Liga table of the current season."

    def bl_table():
        bundesliga_table_link = f"https://onefootball.com/en/competition/bundesliga-1/table"
        bundesliga_table_source = requests.get(bundesliga_table_link).text
        bundesliga_table_page = BeautifulSoup(bundesliga_table_source, "lxml")
        # pos_prem_table = laliga_table_page.find_all("a", class_="standings__cell standings__cell--numeric")
        teams_bundesliga_table = bundesliga_table_page.find_all("p", class_="title-7-medium standings__team-name")
        points_bundesliga_table = bundesliga_table_page.find_all("span", class_="title-7-bold")
        stats_bundesliga_table = bundesliga_table_page.find_all("span", class_="standings__cell-text--dimmed")

        ### Prints columnised table of the Premier League at the moment of command execution ###

        # temp_pos_table = []
        temp_bundesliga_teams_table = []  # Empty table created to be filled later.
        temp_bundesliga_points_table = []
        temp_bundesliga_stats_table = []
        numbers_table = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17',
                         '18', '19',
                         '20']  # List of numbers manually inputted. Will later be changed and have the script automatically fetch these from the site.
        headers = ["Pos", "Team", "GP", "W", "D", "L", "GD", "Pts"]

        # for i in range (len(pos_prem_table)):
        #    temp_pos_table.append(pos_prem_table[i].text.strip())

        for i in range(len(teams_bundesliga_table)):  # For every line temp_tab:
            temp_bundesliga_teams_table.append(
                teams_bundesliga_table[i].text.strip())  # Add a line to temp_table and strip away the formatting.

        for i in range(len(points_bundesliga_table)):
            temp_bundesliga_points_table.append(points_bundesliga_table[i].text.strip())

        for i in range(len(stats_bundesliga_table)):
            temp_bundesliga_stats_table.append(stats_bundesliga_table[i].text.strip())

        #  stats_prem_table returns GP, W, D, L, and GD all in one go. This is why the following function can simply reuse the variable by starting the table count at different rows.
        intermediate_bundesliga_table = zip(numbers_table, temp_bundesliga_teams_table, temp_bundesliga_stats_table[0::5], temp_bundesliga_stats_table[1::5],
                                      temp_bundesliga_stats_table[2::5], temp_bundesliga_stats_table[3::5], temp_bundesliga_stats_table[4::5],
                                      temp_bundesliga_points_table[
                                      1::2])  # Add the two tables together, row for row. The temp_points_table only selected every second entry of the table starting from the first uneven numbers. This is due to how the website is formatted.

        final_bundesliga_table = tabulate(intermediate_bundesliga_table, headers=headers)

        print(final_bundesliga_table)
        return final_bundesliga_table

    await ctx.send(bl_table())

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
