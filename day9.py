from aocd import get_data
import re

data = get_data(year=2018, day=9)

marbles = []

class Marble:
    def __init__(self, number, ccw = None, cw = None):
        self.number = number
        self.ccw = ccw or self
        self.cw = cw or self


def add_marble(marbles, current_marble, index):
    score_to_add = 0
    if current_marble is None:
        m = Marble(index)
    elif index % 23 == 0:
        #Add to score, remove 7 ccw and add to score
        other_score = current_marble.ccw.ccw.ccw.ccw.ccw.ccw.ccw
        clockwise = other_score.cw
        counterclockwise = other_score.ccw
        counterclockwise.cw = clockwise
        clockwise.ccw = counterclockwise
        score_to_add = index + other_score.number
        m = clockwise
    else:
        ccw = current_marble.cw
        cw = current_marble.cw.cw
        m = Marble(number=index, ccw=ccw, cw=cw)
        ccw.cw = m
        cw.ccw = m
    marbles.append(m)
    current_marble = m
    return marbles, current_marble, score_to_add

def run_game(number_of_players, number_of_marbles):
    player_scores = [0 for i in range(number_of_players)]
    cur_player = 0
    marbles = []
    cur_marble = None
    for idx in range(number_of_marbles):
        marbles, cur_marble, score_to_add = add_marble(marbles, cur_marble, idx)
        player_scores[cur_player] = player_scores[cur_player] + score_to_add
        cur_player += 1
        cur_player %= number_of_players
    return player_scores

def part_one(num_players, num_marbles):
    scores = run_game(num_players, num_marbles)
    answer = max(scores)
    return answer

examples = [(10,1618,8317),(13,7999,146373),(17,1104,2764),(21,6111,54718),(30,5807,37305)]
for np,nm,score in examples:
    sc = part_one(np,nm)
    print(sc, score)

answer = part_one(468, 71010)
answer_part_two = part_one(468, 71010*100)