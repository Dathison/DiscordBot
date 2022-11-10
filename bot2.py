import subprocess
import secrets_file
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
import pandas as pd

TOKEN = secrets_file.discord_token

description = '''Piss Bot for the Piss people!'''
bot = commands.Bot(command_prefix='!', description=description)


def league_stats(fbrlink, table, column1, column2, column3, column4, column5):
    html_doc = pd.read_html(fbrlink)
    html_doc1 = pd.DataFrame(html_doc[table])  # Selects the first table of the initial html_doc output.
    html_doc1.columns = html_doc1.columns.droplevel()  # droplevel() removes the line with ''Standard'' and ''Expected'' and leaves just the table.
    headers = ["Squad", column1, column2, column3, column4, column5]
    fetch_stats = list(zip(html_doc1["Squad"], html_doc[column1], html_doc[column2], html_doc[column3], html_doc[column4], html_doc[column5]))

    print(html_doc)

#    print(html_doc[["Squad", column1, column2, column3, column4, column5]])
#    temp_fbref =
#    print(fetch_stats)
    fbref_tab = [html_doc1[["Squad", column1, column2, column3, column4, column5]]]

    for i in range(len(fetch_stats)):
        fbref_tab.append(fetch_stats[i])

    #final_stats_table = tabulate(fbref_tab, headers=headers)

    #print(final_stats_table)
    #return final_stats_table
    return fbref_tab

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
async def test_stats(ctx):

    html_doc = pd.read_html('https://fbref.com/en/comps/9/Premier-League-Stats')
    print(html_doc)

@bot.command()
async def pl_shooting(ctx):

    "Shot stats and analysis for every Premier League team."

    print("Start fetch.")
    await ctx.send(f" ``` {league_stats('https://fbref.com/en/comps/9/shooting/Premier-League-Stats',0,'Gls','Sh','Sh/90','SoT','SoT%')} ``` ")
    print("Fetch finished.")

@bot.command()
async def pl(ctx):

    "Test for advanced stats."
    print("-----------------")
    print("Start fetch.")
    await ctx.send(f" ``` {league_stats('https://fbref.com/en/comps/9/Premier-League-Stats',6,'90s','Cmp','Launch%','#OPA/90','AvgDist')} ``` ")
    print("Fetch finished.")

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

    "Show the Premier League table of the current season."

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
        numbers_table = []  # List of numbers manually inputted. Will later be changed and have the script automatically fetch these from the site.
        notes = []
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
## TEST ##
#            notes.append("")
#            if temp_prem_table[4::5][int((i-1)/4)] == -5:
#                notes[i-1].append("Shite.")


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

    "Shows the Bundesliga table of the current season."

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

    "Show the Championship table of the current season."

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

    "Show the Champions League table of the current season."
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

        print(chle_table.first_final_cl_table)
        print("--------------------------------")
        print(chle_table.second_final_cl_table)

    chle_table()

    await ctx.send(f"``` {chle_table.first_final_cl_table} ``` ")
    await ctx.send(f"``` {chle_table.second_final_cl_table} ```")

#@bot.command()
#async def shutdown(self,ctx):
#    if ctx.message.author.id == 150634514035507200: #replace OWNERID with your user id
#      print("shutdown")
#      try:
#        await self.bot.logout()
#      except:
#        print("EnvironmentError")
#        self.bot.clear()
#    else:
#      await ctx.send("You do not own this bot!")

@bot.command()
async def fixtures(ctx):

    "Show the fixtures of Spurs for the current month."

    fhtml_doc = pd.read_html('https://fbref.com/en/squads/361ca564/Tottenham-Hotspur-Stats')
    fhtml_doc1 = pd.DataFrame(fhtml_doc[1])  # Selects the first table of the initial html_doc output.
    fhtml_doc1 = fhtml_doc1.fillna("")

    spurs_list = ["Tottenham"] * 40
    noscore_list = ["x"] * 40
    home_list = list(zip(fhtml_doc1["Comp"],fhtml_doc1["Date"],fhtml_doc1["Time"],spurs_list,int(fhtml_doc1["GF"]),int(fhtml_doc1["GA"]),fhtml_doc1["Opponent"]))
    away_list = list(zip(fhtml_doc1["Comp"],fhtml_doc1["Date"],fhtml_doc1["Time"],fhtml_doc1["Opponent"],fhtml_doc1["GF"],fhtml_doc1["GA"],spurs_list))
    notplayed_list = list(zip(fhtml_doc1["Comp"],fhtml_doc1["Date"],fhtml_doc1["Time"],spurs_list,noscore_list,noscore_list,fhtml_doc1["Opponent"]))

    fixtures_fbref_tab = []

    for i in range(len(fhtml_doc1)):

        if fhtml_doc1["GF"][i] == None:
            fixtures_fbref_tab.append(notplayed_list[i])

        elif fhtml_doc1["Venue"][i] == "Home":
            fixtures_fbref_tab.append(home_list[i])

        else:
            fixtures_fbref_tab.append(away_list[i])

    fixtures_len = len(fixtures_fbref_tab)

    fixtures_divisor = fixtures_len//2

    first_fixtures = fixtures_fbref_tab[:fixtures_divisor]
    second_fixtures = fixtures_fbref_tab[fixtures_divisor:]

    headers = ["Competition","Date","Time","Home","","","Away"]

    first_final_fixtures = tabulate(first_fixtures, headers=headers)
    second_final_fixtures = tabulate(second_fixtures, headers=headers)

    await ctx.send(f" ``` {first_final_fixtures} ``` ")
    await ctx.send(f" ``` {second_final_fixtures} ``` ")

@bot.command()
async def injuries(ctx):
	page = 'https://www.transfermarkt.com/tottenham-hotspur/sperrenundverletzungen/verein/148'
	request = requests.get(page, headers={'User-Agent': 'Custom5'})
	response = request.text
	injuries = pd.read_html(response)
	inj_df = pd.DataFrame(injuries[0])  # Selects the first table of the initial html_doc output.
#	inj_df = inj_df.fillna('')
#	inj_df = inj_df.style.hide_index()

	inj_player = []
	inj_reason = []
	inj_since = []
	inj_return = []
	inj_missed = []

	age_clm = inj_df["Age"][inj_df.index % 3 == 2]
	rsn_clm = inj_df["Reason"][inj_df.index % 3 == 1]
	snc_clm = inj_df["since"][inj_df.index % 3 == 1]
	ret_clm = inj_df["Expected return"][inj_df.index % 3 == 1]
	mis_clm = inj_df["Missed matches"][inj_df.index % 3 == 1]

#	for i in range(len(inj_df["Age"][inj_df.index % 3 == 2])):
	inj_player.append(age_clm)

#	for i in range(len(inj_df["Reason"][inj_df.index % 3 == 1])):
	inj_reason.append(rsn_clm)

#	for i in range(len(inj_df["since"][inj_df.index % 3 == 1])):
	inj_since.append(snc_clm)

#	for i in range(len(inj_df["Expected return"][inj_df.index % 3 == 1])):
	inj_return.append(ret_clm)

#	for i in range(len(inj_df["Missed matches"][inj_df.index % 3 == 1])):
	inj_missed.append(mis_clm)

	tmp_inj_table = list(zip(inj_player, inj_reason, inj_since, inj_return, inj_missed))

	headers = ["Player","Reason","Since","Return","Matches missed"]
	inj_table = tabulate(tmp_inj_table, headers=headers)

#	await ctx.send(f" ``` {tmp_inj_table} ``` ")
#	print(injuries)
	print(inj_table)

#@bot.command()
#async def pisstest(ctx):
#    await ctx.send(f"This is a test string. Please type ''a'' or ''b''")

#    def check(msg):
# 	        msg.content.lower() in ["a", "b"]

#    msg = await bot.wait_for("message", timeout=30)
#    if msg.content() == "a" or msg.content() == "b":
#        await ctx.send("Success!")
#    else:
#        await ctx.send("Failed!")

bot.run(TOKEN)
