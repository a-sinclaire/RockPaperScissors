# Amelia Sinclaire 2023
import random
from enum import Enum
import numpy as np
import logging
logging.basicConfig(format='%(message)s', level=logging.ERROR)
import Strategies

State = Enum('State', ['HUMAN_WINS', 'COMPUTER_WINS', 'TIE'])
Throws = Enum('Throw', ['ROCK', 'PAPER', 'SCISSORS', 'EXIT'])


class Rounds:
    rounds = []

    def __init__(self, rounds=None):
        Rounds.rounds = rounds if rounds is not None else []

    def add_round(self, r):
        self.rounds.append(r)

    def display_rounds(self):
        for idx, r in enumerate(self.rounds):
            print(f'[{idx}] ({r.p1.name}, {r.p2.name}, {r.outcome.name})')

    def empty(self):
        return len(self.rounds) == 0

    def opponent_last_move(self):
        return self.rounds[-1].p1

    def get_throws_in_outcome(self, computer=True, outcome=State['TIE'], previous_n_rounds=None):
        n = 0 if previous_n_rounds is None else -previous_n_rounds
        throws = []
        for r in self.rounds[n:]:
            if r.outcome.value == outcome.value:
                if computer:
                    throws.append(r.p2)
                else:
                    throws.append(r.p1)
        return throws

    def get_throws(self, player=True, previous_n_rounds=None):
        n = 0 if previous_n_rounds is None else -previous_n_rounds
        throws = []
        for r in self.rounds[n:]:
            if player:
                throws.append(r.p1)
            else:
                throws.append(r.p2)
        return throws

    def get_rounds(self, previous_n_rounds=None):
        n = 0 if previous_n_rounds is None else -previous_n_rounds
        rounds = []
        for r in self.rounds[n:]:
            rounds.append(r)
        return rounds

    def percent_outcome(self, outcome, previous_n_rounds=None):
        if self.empty():
            return 0
        return 100*len(self.get_throws_in_outcome(True, outcome, previous_n_rounds)) / len(self.rounds)

    def display_percentages(self):
        if self.empty():
            return
        percent_wins = self.percent_outcome(State['HUMAN_WINS'])
        percent_ties = self.percent_outcome(State['TIE'])
        percent_loss = self.percent_outcome(State['COMPUTER_WINS'])
        ratio = str(f' | Ratio: {percent_wins/percent_loss:.2f}') if percent_loss > 0 else ""
        print(f'Win: {percent_wins:.2f}% | Lose: {percent_loss:.2f}% | Tie: {percent_ties:.2f}%{ratio} | ({len(self.rounds)} Rounds)')


class Round:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.outcome = evaluate_game(p1, p2)

    def display_round(self):
        print(f'p1: {self.p1.name}')
        print(f'p2: {self.p2.name}')
        print(self.outcome.name)

    def display_oneline(self):
        print(f'({self.p1.name}, {self.p2.name}, {self.outcome.name})')


def random_throw():
    return random.choice(list(Throws)[0:3])


def normalize(v):
    v = np.asarray(v)
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm


def validate_throw(t):
    throw = t.upper()
    for t in Throws:
        if throw == t.name:
            return t
    match throw:
        case "R": return Throws['ROCK']
        case "P": return Throws['PAPER']
        case "S": return Throws['SCISSORS']
        case _: return None


def evaluate_game(p1, p2):
    if p1.value == p2.value:
        return State['TIE']
    if p1.value == Throws['ROCK'].value:
        if p2.value == Throws['PAPER'].value:
            return State['COMPUTER_WINS']
        return State['HUMAN_WINS']
    if p1.value == Throws['PAPER'].value:
        if p2.value == Throws['SCISSORS'].value:
            return State['COMPUTER_WINS']
        return State['HUMAN_WINS']
    if p2.value == Throws['ROCK'].value:
        return State['COMPUTER_WINS']
    return State['HUMAN_WINS']


def main(all_rounds):
    computer = Strategies.SameliaBot(computer=True, depth=0)  # "computer" / p2
    comp2 = Strategies.SwitchAfterTwo(computer=False)  # "human" / p1
    import math, time

    def loop(all_rounds, max_rounds=math.inf):
        if max_rounds == 0:
            exit()
        # Get Computer Throw
        p2_throw = computer.throw()
        # p2_throw = computer.counter_throw(computer.counter_strat(Strategies.BeatMostFreq)['opponent_next_throw'])#computer.throw()

        # Get Player Throw
        # p1_throw = comp2.counter_throw(comp2.counter_strat(Strategies.SameliaBot)['opponent_next_throw'])#computer.throw()
        p1_throw = None
        while p1_throw is None:
            p1_throw = input("What will you Throw? > ")
            p1_throw = validate_throw(p1_throw)
        if p1_throw.value == Throws['EXIT'].value:
            print('exiting program')
            exit()
        this_round = Round(p1_throw, p2_throw)
        this_round.display_round()
        all_rounds.add_round(this_round)
        # all_rounds.display_rounds()
        all_rounds.display_percentages()

        computer.update(all_rounds)
        comp2.update(all_rounds)

        loop(all_rounds, max_rounds-1)

    loop(all_rounds, max_rounds=500)


if __name__ == "__main__":
    all_rounds = Rounds()
    main(all_rounds)
