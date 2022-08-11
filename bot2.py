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

    await ctx.send(f'``` {ll_table()} ```')

@bot.command()
async def pl_table(ctx):

    def pl_table():
        prem_table_link = f"https://onefootball.com/en/competition/premier-league-9/table"
        prem_table_source = requests.get(prem_table_link).text
        prem_table_page = BeautifulSoup(prem_table_source, "lxml")
        #pos_prem_table = prem_table_page.find_all("a", class_="standings__cell standings__cell--numeric")
        teams_prem_table = prem_table_page.find_all("p", class_="title-7-medium standings__team-name")
        points_prem_table = prem_table_page.find_all("span", class_="title-7-bold")
        temp_prem_table = prem_table_page.find_all("span", class_="standings__cell-text--dimmed")

        ### Prints columnised table of the Premier League at the moment of command execution ###

        #temp_pos_table = []
        temp_teams_table = []  # Empty table created to be filled later.
        temp_points_table = []
        temp_stats_table = []
#        temp_gp_table = [temp_prem_table[0::5]]
#        temp_w_table = [temp_prem_table[1::5]]
#        temp_d_table = [temp_prem_table[2::5]]
#        temp_l_table = [temp_prem_table[3::5]]
#        temp_gd_table = [temp_prem_table[4::5]]
        numbers_table = []  # List of numbers manually inputted. Will later be changed and have the script automatically fetch these from the site.
        headers = ["Pos","Team", "GP", "W", "D", "L", "GD", "Pts"]

        numbers_table = list(range(1, len(teams_prem_table)+1))

        #for i in range (len(pos_prem_table)):
        #    temp_pos_table.append(pos_prem_table[i].text.strip())

#        temp_prem_table.text.strip()

        for i in range(len(teams_prem_table)):  # For every line temp_tab:
            temp_teams_table.append(teams_prem_table[i].text.strip())  # Add a line to temp_table and strip away the formatting.

        for i in range(len(points_prem_table)):
            temp_points_table.append(points_prem_table[i].text.strip())

        for i in range(len(temp_prem_table)):
            temp_stats_table.append(temp_prem_table[i].text.strip())

#        for i in range(len(temp_prem_table[1::5])):
#            temp_w_table.append(temp_prem_table[1::5][i])

#        for i in range(len(temp_prem_table[2::5])):
#            temp_d_table.append(temp_prem_table[2::5][i])

#        for i in range(len(temp_prem_table[3::5])):
#            temp_l_table.append(temp_prem_table[3::5][i])

#        for i in range(len(temp_prem_table[4::5])):
#            temp_gd_table.append(temp_prem_table[4::5][i])

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

    await ctx.send(f'``` {bl_table()} ```')

@bot.command()
async def champ_table(ctx):

    def cs_table():
        cs_table_link = f"https://onefootball.com/en/competition/the-championship-27/table"
        cs_table_source = requests.get(cs_table_link).text
        cs_table_page = BeautifulSoup(cs_table_source, "lxml")
        teams_cs_table = cs_table_page.find_all("p", class_="title-7-medium standings__team-name")
        points_cs_table = cs_table_page.find_all("span", class_="title-7-bold")
        temp_cs_table = cs_table_page.find_all("span", class_="standings__cell-text--dimmed")

        ### Prints columnised table of the Premier League at the moment of command execution ###

        temp_cs_teams_table = []  # Empty table created to be filled later.
        temp_cs_points_table = []
        temp_cs_stats_table = []
        numbers_table = []  # List of numbers manually inputted. Will later be changed and have the script automatically fetch these from the si>
        headers = ["Pos","Team", "GP", "W", "D", "L", "GD", "Pts"]

        cs_numbers_table = list(range(1, len(teams_cs_table)+1))

        for i in range(len(teams_cs_table)):  # For every line temp_tab:
            temp_cs_teams_table.append(teams_cs_table[i].text.strip())  # Add a line to temp_table and strip away the formatting.

        for i in range(len(points_cs_table)):
            temp_cs_points_table.append(points_cs_table[i].text.strip())

        for i in range(len(temp_cs_table)):
            temp_cs_stats_table.append(temp_cs_table[i].text.strip())

        intermediate_cs_table = zip(cs_numbers_table, temp_cs_teams_table, temp_cs_stats_table[0::5], temp_cs_stats_table[1::5], temp_cs_stats_table[2::5], temp_cs_stats_table[3::5], temp_cs_stats_table[4::5], temp_cs_points_table[1::2])

        final_cs_table = tabulate(intermediate_cs_table, headers=headers)

        print(final_cs_table)
        return final_cs_table

    await ctx.send(f'``` {cs_table()} ```')

@bot.command()
async def cl_table(ctx):

    def chle_table():

        cl_table_link = f"https://onefootball.com/en/competition/champions-league-5/table"
        cl_table_source = requests.get(cl_table_link).text
        cl_table_page = BeautifulSoup(cl_table_source, "lxml")
        temp_cl_groups = cl_table_page.find_all("p",class_="label standings__table-header-text")
        temp_cl_teams = cl_table_page.find_all("p",class_="title-7-medium standings__team-name")
        temp_cl_stats = cl_table_page.find_all("span", class_="title-7-medium standings__cell-text--dimmed")
        temp_cl_points = cl_table_page.find_all("span", class_="title-7-bold")  # Includes positions on even numbered keys and points on odd numbered keys.


        group_cl = []
        teams_cl = []
        stats_cl = []
        points_cl = []

        headers = ["Pos","Team", "GP", "W", "D", "L", "GD", "Pts"]

        for i in range(len(temp_cl_groups)):
            group_cl.append(temp_cl_groups[i].text.strip())

            for x in range(int(len(temp_cl_teams) / len(temp_cl_groups)) - 1):
                group_cl.append("")

        for i in range(len(temp_cl_teams)):
            teams_cl.append(temp_cl_teams[i].text.strip())

        for i in range (len(temp_cl_stats)):
            stats_cl.append(temp_cl_stats[i].text.strip())

        for i in range (len(temp_cl_points)):
            points_cl.append(temp_cl_points[i].text.strip())

        group_len = len(group_cl)
        teams_len = len(teams_cl)
        stats_len = len(stats_cl)
        points_len = len(points_cl)

        group_divisor = group_len//2
        teams_divisor = teams_len//2
        stats_divisor = stats_len//2
        points_divisor = points_len//2

        first_group_cl = group_cl[:group_divisor]
        first_teams_cl = teams_cl[:teams_divisor]
        first_stats_cl = stats_cl[:stats_divisor]
        first_points_cl = points_cl[:points_divisor]
        second_group_cl = group_cl[group_divisor:]
        second_teams_cl = teams_cl[teams_divisor:]
        second_stats_cl = stats_cl[stats_divisor:]
        second_points_cl = points_cl[points_divisor:]

        first_intermediate_cl_table = zip(first_group_cl, first_points_cl[0::2], first_teams_cl,  first_stats_cl[0::5], first_stats_cl[1::5], first_stats_cl[2::5], first_stats_cl[3::5], first_stats_cl[4::5], first_points_cl[1::2])
        second_intermediate_cl_table = zip(second_group_cl, second_points_cl[0::2], second_teams_cl,  second_stats_cl[0::5], second_stats_cl[1::5], second_stats_cl[2::5], second_stats_cl[3::5], second_stats_cl[4::5], second_points_cl[1::2])

        chle_table.first_final_cl_table = tabulate(first_intermediate_cl_table, headers=headers)
        chle_table.second_final_cl_table = tabulate(second_intermediate_cl_table, headers=headers)

    chle_table()

    await ctx.send(f"``` {chle_table.first_final_cl_table} ``` ")
    await ctx.send(f"``` {chle_table.second_final_cl_table} ```")

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
