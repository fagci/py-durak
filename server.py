#!/usr/bin/env python3

from random import randint, seed, shuffle


class CardsTypeStandard:
    NOMINALS = ('6', '7', '8', '9', '10', 'В', 'Д', 'К', 'Т')
    SUIT = ('♠', '♥', '♣', '♦')


class Deck(list[tuple]):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trump = kwargs.get('trump', (None, None))

    def set_trump(self, trump):
        self.trump = trump

    @property
    def sorted(self):
        _, ts = self.trump

        def key(v):
            n, s = v
            return (
                1 if s == ts else 0,
                CardsTypeStandard.NOMINALS.index(n),
                s,
            )
        return Deck(sorted(self, key=key), trump=self.trump)

    def __repr__(self):
        return ' '.join('%s%s' % c for c in self)

    def __str__(self):
        return self.__repr__()

    def rotate(self, i: int = 1):
        part = self.slice(i)
        self.extend(part)

    def slice(self, n):
        part = self[:n]
        del self[:n]
        return part


class Player:
    def __init__(self, name):
        self.name = name
        self._cards = Deck()

    def add_cards(self, cards):
        self._cards.extend(cards)
        self.resort()

    def resort(self):
        self._cards = self._cards.sorted

    def get_small_card(self):
        card = self._cards[0]
        del self._cards[0]
        return card

    def get_beat_card(self, card):
        _, ts = self._cards.trump
        nom = CardsTypeStandard.NOMINALS
        cn, cs = card
        for beat_card in self._cards:
            bn, bs = beat_card
            larger = bs == cs and nom.index(cn) < nom.index(bn)
            trump_beat = bs == ts and cs != ts
            # print(beat_card, larger, trump_beat, self.cards.trump)
            if larger or trump_beat:
                self._cards.remove(beat_card)
                return beat_card

    def set_trump(self, trump):
        self._cards.set_trump(trump)
        self.resort()

    @property
    def cards(self):
        return self._cards

    @property
    def has_cards(self):
        return bool(self._cards)

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return '%s: %s' % (self.name, self.sorted_str)

    @property
    def sorted_str(self):
        return ' '.join('%s%s' % c for c in self.cards)


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

        self.attacker = self.defender
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
    seed(1)
    game = CardGame(Durak())
    for _ in range(3):
        game.newplayer()
    game.play()


if __name__ == "__main__":
    main()
