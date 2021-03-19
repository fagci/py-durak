from cardgame.deck import Deck


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
        return self._cards.get_beat_card(card)

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
        return str(self.cards)
