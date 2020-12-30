import sys
sys.path.append(".")
from game_stats import GameStats

class Game:
    def __init__(self, opponent):
        self.opponent = opponent
        self.win = False
        self.loss = False
        self.tie = False
        self.totalRankingPoints = 0
        self.driveRankingPoints = 0
        self.resultRankingPoints = 0
        self.stats = GameStats()
