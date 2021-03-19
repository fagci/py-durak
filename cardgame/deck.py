class DeckType:
    _NOM = ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')
    _SUIT = ('♠', '♥', '♣', '♦')
    NOM = _NOM
    SUIT = _SUIT
    _GRAPH = (
        ('🂡', '🂢', '🂣', '🂤', '🂥', '🂦', '🂧', '🂨', '🂩', '🂪', '🂫', '🂭', '🂮'),
        ('🂱', '🂲', '🂳', '🂴', '🂵', '🂶', '🂷', '🂸', '🂹', '🂺', '🂻', '🂽', '🂾'),
        ('🃁', '🃂', '🃃', '🃄', '🃅', '🃆', '🃇', '🃈', '🃉', '🃊', '🃋', '🃍', '🃎'),
        ('🃑', '🃒', '🃓', '🃔', '🃕', '🃖', '🃗', '🃘', '🃙', '🃚', '🃛', '🃝', '🃞'),
    )

    @classmethod
    def graph(cls, card):
        nominal, suit = card
        suit_index = cls._SUIT.index(suit)
        nom_index = cls._NOM.index(nominal)
        return cls._GRAPH[suit_index][nom_index]


class DeckTypeRus(DeckType):
    NOM = ('6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')
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
                DeckTypeRus.NOM.index(n),
                s,
            )
        return Deck(sorted(self, key=key), trump=self.trump)

    def get_beat_card(self, card):
        _, ts = self.trump
        nom = DeckTypeRus.NOM
        cn, cs = card
        for beat_card in self:
            bn, bs = beat_card
            larger = bs == cs and nom.index(cn) < nom.index(bn)
            trump_beat = bs == ts and cs != ts
            # print(beat_card, larger, trump_beat, self.cards.trump)
            if larger or trump_beat:
                self.remove(beat_card)
                return beat_card

    def __repr__(self):
        return ' '.join(DeckType.graph(c) for c in self)

    def __str__(self):
        return self.__repr__()

    def rotate(self, i: int = 1):
        part = self.slice(i)
        self.extend(part)

    def slice(self, n):
        part = self[:n]
        del self[:n]
        return part
