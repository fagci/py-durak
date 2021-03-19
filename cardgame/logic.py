from random import shuffle
from cardgame.deck import Deck, CardsTypeRus
from cardgame.player import Player


class Durak(CardsTypeRus):
    def __init__(self):
        self.deck = Deck()
        for n in self.NOM:
            for s in self.SUIT:
                self.deck.append((n, s))

        shuffle(self.deck)
        self.field = {}
        self.attacker = None
        self.defender = None

    def init_players(self, players: list[Player]):
        self.players = players
        players_count = len(players)
        cards_per_player = min(6, len(self.deck) // players_count)

        cards = []
        for player in players:
            cards = self.deck[:cards_per_player]
            player.add_cards(cards)
            del self.deck[:cards_per_player]

        if self.deck:
            self.trump = self.deck[0]
            self.deck.rotate()
        else:
            self.trump = cards[-1]

        for player in players:
            player.set_trump(self.trump)

        print('Trump: %s%s' % self.trump)
        print(repr(self.deck))

    @property
    def players_w_cards(self):
        return list(filter(lambda p: p.has_cards, self.players))

    def get_durak(self):
        w_cards = self.players_w_cards
        w_cards_count = len(w_cards)
        if w_cards_count > 1:
            return
        return w_cards[0] if w_cards_count else False

    def play(self):
        durak = None
        round_num = 0
        while durak is None:
            round_num += 1
            print('>> Round', round_num)
            self.play_round()
            durak = self.get_durak()

        print('Durak:', durak)

    def play_round(self):
        players = self.players_w_cards
        print('Deck:', self.deck.__str__())
        for p in self.players:
            print(p)

        if not self.attacker:
            self.attacker = players[0]

        if not self.defender:
            # TODO: fix
            attacker_index = players.index(self.attacker)
            self.defender = players[(attacker_index + 1) % len(players)]

        print(self.attacker.name, '>', self.defender.name)

        winner = None
        while winner is None:
            winner = self.iter()

        for p in self.players_w_cards:
            print(p)

        for p in players:
            if self.deck:
                need = 6 - len(p.cards)
                if need > 0:
                    p.add_cards(self.deck.slice(need))

        self.attacker = winner
        self.defender = None

    def iter(self):
        card = self.attacker.get_small_card()
        beat = self.defender.get_beat_card(card)
        print('%s%s' % card)
        print('%s%s' % beat if beat else 'fail')
        if not beat:
            self.defender.add_cards([card])
            return self.attacker
        else:
            self.field[card] = beat
            return self.defender
