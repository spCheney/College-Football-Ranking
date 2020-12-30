import sys
sys.path.append(".")
from game import Game

class Team:
    def __init__(self, name, id):
        self.id = id
        self.name = name
        self.preseasonPoints = 0
        self.seasonPoints = 0
        self.games = []
        self.wins = 0
        self.loses = 0
        self.ties = 0

    def addGame(self, opponent):
        self.games.append(Game(opponent))

    def findIndexOfGame(self, opponent):
        for i in range(len(self.games)):
            if self.games[i].opponent.id == opponent.id:
                return i

        else:
            self.addGame(opponent)
            return (len(self.games) - 1)

    def addDrivePoints(self, opponent, points):
        self.games[self.findIndexOfGame(opponent)].driveRankingPoints += points

    def getDrivePoints(self, opponent):
        return self.games[self.findIndexOfGame(opponent)].driveRankingPoints

    def addGameResultPoints(self, opponent, points):
        self.games[self.findIndexOfGame(opponent)].resultRankingPoints += points

    def getGameResultPoints(self, opponent):
        return self.games[self.findIndexOfGame(opponent)].resultRankingPoints

    def calcGameResultPoints(self, opponent):
        gameIndex = self.findIndexOfGame(opponent)
        opponentGameIndex = opponent.findIndexOfGame(self)

        if self.games[gameIndex].stats.points > opponent.games[opponentGameIndex].stats.points:
            self.wins += 1
            self.games[gameIndex].win = True
        elif self.games[gameIndex].stats.points < opponent.games[opponentGameIndex].stats.points:
            self.loses += 1
            self.games[gameIndex].loss = True
        elif self.games[gameIndex].stats.points == opponent.games[opponentGameIndex].stats.points:
            self.ties += 1
            self.games[gameIndex].tie = True
        
        dop = (self.games[gameIndex].stats.points - opponent.games[opponentGameIndex].stats.points) * 10
        if opponent.games[opponentGameIndex].stats.points == 0:
            dop = dop * 2

        doy = self.games[gameIndex].stats.yards - opponent.games[opponentGameIndex].stats.yards
    
        posPer = 0.5
        if self.games[gameIndex].stats.timeOfPossession + opponent.games[opponentGameIndex].stats.timeOfPossession != 0:
            posPer = float(self.games[gameIndex].stats.timeOfPossession) / float(self.games[gameIndex].stats.timeOfPossession + opponent.games[opponentGameIndex].stats.timeOfPossession)

        fdRank = self.games[gameIndex].stats.firstDowns / 10

        penRank = self.games[gameIndex].stats.penalties + (self.games[gameIndex].stats.penaltyYards / 10)

        self.games[gameIndex].resultRankingPoints +=  (((dop + doy) * posPer) + fdRank - penRank)

    def updateGameStats(self, opponent, gameStats):
        self.games[self.findIndexOfGame(opponent)].stats = gameStats

    def calculateTotalRankingPoints(self):
        for game in self.games:
            drivePointsDif = (game.driveRankingPoints - game.opponent.getDrivePoints(self)) / 2
            resultPointsDif = (game.resultRankingPoints - game.opponent.getGameResultPoints(self)) / 2
            game.totalRankingPoints = (drivePointsDif + resultPointsDif)

    def getTotalRankingPoints(self):
        total = 0
        for game in self.games:
            total += game.totalRankingPoints

        return total

    def calculateSeasonPoints(self):
        if len(self.games) > 0:
            recordPerc = float(self.wins) / float(self.wins + self.loses + self.ties)
            self.seasonPoints = self.getTotalRankingPoints() / len(self.games)
            recordPoints = 0

            for game in self.games:
                # chance of winning (cow)
                points = self.getTotalRankingPoints() / len(self.games)
                opponentsPoints = game.opponent.getTotalRankingPoints() / len(game.opponent.games)
                cow = (points - opponentsPoints) / 1000
                if cow < 0:
                    cow = (1 - cow) / 2
                else:
                    cow = 0.5 + (cow / 2)

                overUnder = 0
                if cow > 50:
                    overUnder = (cow - 0.5) * 21
                else:
                    overUnder = 0 - (cow * 21)
                print(overUnder)
                if game.win:
                    recordPoints += 100
                elif game.loss:
                    recordPoints -= 100
                elif game.tie:
                    recordPoints += 50


    def avgOpptSeasonPts(self):
        total = 0
        for game in self.games:
            print(game.opponent.name)
            print(game.opponent.seasonPoints)
            total += game.opponent.seasonPoints

        return total / len(self.games)
