from cardgame.player import Player


class CardGame:
    def __init__(self, logic):
        self.players = []
        self.players_count = 0
        self.logic = logic

    def newplayer(self):
        num = len(self.players) + 1
        name = 'Player %d' % num
        player = Player(name)
        self.players.append(player)
        self.players_count += 1

    def play(self):
        self.logic.init_players(self.players)

        for player in self.players:
            print(player)

        self.logic.play()
