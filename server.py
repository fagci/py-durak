#!/usr/bin/env python3

from random import shuffle


class CardsTypeStandard:
    NOMINALS = ('6', '7', '8', '9', '10', 'В', 'Д', 'К', 'Т')
    SUIT = ('♠', '♥', '♣', '♦')


class Deck(list[tuple]):
    @property
    def sorted(self):
        def key(v):
            n, s = v
            return CardsTypeStandard.NOMINALS.index(n), s
        return sorted(self, key=key)

    def __repr__(self):
        return ' '.join('%s%s' % c for c in self)

    def __str__(self):
        return self.__repr__()

    @property
    def sorted_str(self):
        return ' '.join('%s%s' % c for c in self.sorted)

    def rotate(self, i: int = 1):
        part = self[:i]
        del self[:i]
        self.extend(part)


class Player:
    def __init__(self, name):
        self.name = name
        self._cards = Deck()

    def add_cards(self, cards):
        self._cards.extend(cards)

    @property
    def cards(self):
        return self._cards[:]

    @property
    def has_cards(self):
        return bool(self._cards)

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return '%s: %s' % (self.name, self._cards.sorted_str)


class Durak(CardsTypeStandard):
    def __init__(self):
        self.deck = Deck()
        for n in self.NOMINALS:
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
        for p in self.players_w_cards:
            p._cards.pop()
        for p in self.players_w_cards:
            print(p)


class CardGame:
    def __init__(self, logic: Durak):
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


def main():
    game = CardGame(Durak())
    for _ in range(3):
        game.newplayer()
    game.play()


if __name__ == "__main__":
    main()
