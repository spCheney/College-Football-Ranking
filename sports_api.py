import requests
from datetime import datetime

from team import Team
from game_stats import GameStats

def findTeamIndexByName(name):
    global teams
    for i in teams:
        if i.name == name:
            return i.id

    else:
        return 0

def calcDriveRanking(drive):
    global teams
    oyg = drive['yards']
    yfog = 100 - drive['end_yards_to_goal']
    yardsRank = (oyg + (2 * yfog)) / 3
    resultRank = 0
    result = drive['drive_result']

    if result == "TD":
        resultRank = 3
    elif result == "FG":
        resultRank = 2
    elif "FUMBLE" in result or "INT" in result or "DOWNS" in result:
        resultRank = 0.5
        defBoost = 10
        if "TD" in result:
           defBoost = 30
        teams[findTeamIndexByName(drive['defense'])].addDrivePoints(teams[findTeamIndexByName(drive['offense'])], defBoost)
    else:
        resultRank = 1

    drivePoints = ((yardsRank * resultRank) / 10)
    teams[findTeamIndexByName(drive['offense'])].addDrivePoints(teams[findTeamIndexByName(drive['defense'])], drivePoints)

def calcGameResultsRanking(game):
    global teams

    indexes = []
    gameStatsList = []

    for stats in game:
        gameStats = GameStats()
        indexes.append(findTeamIndexByName(stats['school']))
        gameStats.points = stats['points']
        for stat in stats['stats']:
            if stat['category'] == "totalYards":
                gameStats.yards = int(stat['stat'])
            elif stat['category'] == "totalPenaltiesYards":
                penalties = stat['stat'].split("-")
                gameStats.penalties = int(penalties[0])
                gameStats.penaltyYards = int(penalties[1])
            elif stat['category'] == "firstDowns":
                gameStats.firstDowns = int(stat['stat'])
            elif stat['category'] == "possessionTime":
                time = stat['stat'].split(":")
                minutes = int(time[0])
                seconds = int(time[1])
                gameStats.timeOfPossession = (minutes * 60) + seconds
                break

        gameStatsList.append(gameStats)

    teams[indexes[0]].updateGameStats(teams[indexes[1]], gameStatsList[0])
    teams[indexes[1]].updateGameStats(teams[indexes[0]], gameStatsList[1])

    teams[indexes[0]].calcGameResultPoints(teams[indexes[1]])
    teams[indexes[1]].calcGameResultPoints(teams[indexes[0]])

def getTeams(year):
    global teams
    response = requests.get("https://api.collegefootballdata.com/teams/fbs?year=" + str(year))
    teamData = response.json()
    id = 1
    for data in teamData:
        team = Team(data['school'], id)
        teams.append(team)
        id += 1

def findMostPoints():
    global teams

    bestTeam = Team("temp", 0)
    for i in teams:
        if i.seasonPoints > bestTeam.seasonPoints:
            bestTeam = i
        if i.seasonPoints > 150:
            print(i.name)
            print(i.seasonPoints)
            print(str(i.wins) + "-" + str(i.loses) + "-" + str(i.ties))
            print(i.avgOpptSeasonPts())

    # print(bestTeam.name)
    # print(bestTeam.seasonPoints)

def calcRankings():
    global teams
    for team in teams:
        team.calculateTotalRankingPoints()

    for team in teams:
        team.calculateSeasonPoints()

    teams[findTeamIndexByName("Alabama")].avgOpptSeasonPts()

    # findMostPoints()

teams = []
notFBS = Team("notFBS", 0)
teams.append(notFBS)
getTeams(datetime.today().year)

for week in range(1, 17):
    print(week)
    response = requests.get("http://api.collegefootballdata.com/drives?seasonType=regular&year=2020&week=" + str(week))
    drivesList = response.json()
    for drive in drivesList:
        calcDriveRanking(drive)

    response = requests.get("https://api.collegefootballdata.com/games/teams?year=2020&week=" + str(week) + "&seasonType=regular")
    games = response.json()
    for i in games:
        calcGameResultsRanking(i['teams'])

# teams[findTeamIndexByName("Alabama")].calculateTotalRankingPoints()
# print("Total")
# print(teams[findTeamIndexByName("Alabama")].getTotalRankingPoints())
calcRankings()

# findMostPoints()
