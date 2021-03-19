from cardgame.player import Player


class CardGame:
    def __init__(self, logic):
        self.players = []
        self.players_count = 0
        self.logic = logic

    def newplayer(self):
        num = len(self.players) + 1
        player = Player('Player %d' % num)
        self.players.append(player)
        self.players_count += 1
        return player

    def play(self):
        self.logic.init_players(self.players)
        self.logic.play()
