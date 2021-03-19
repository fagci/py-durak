#!/usr/bin/env python3
from random import seed
from cardgame.logic import Durak
from cardgame.game import CardGame


def main():
    seed(1)
    game = CardGame(Durak())
    for _ in range(3):
        game.newplayer()
    game.play()


if __name__ == "__main__":
    main()
