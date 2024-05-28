import random

# Example Strategies
def always_cooperate(my_history, opponent_history, round_number, relative_score, opponent_reputation):
    return 'C'

def always_defect(my_history, opponent_history, round_number, relative_score, opponent_reputation):
    return 'D'

def tit_for_tat(my_history, opponent_history, round_number, relative_score, opponent_reputation):
    if round_number == 1:
        return 'C'
    else:
        return opponent_history[-1]

def score_based_strategy(my_history, opponent_history, round_number, relative_score, opponent_reputation):
    if round_number == 1:
        return 'C'
    if relative_score > 0:
        return 'C'
    return 'D'

def reputation_based_strategy(my_history, opponent_history, round_number, relative_score, opponent_reputation):
    if round_number == 1:
        return 'C'
    if opponent_reputation < -10:
        return 'N'
    if relative_score > 0:
        return 'C'
    return 'D'

def nuclear_option_strategy(my_history, opponent_history, round_number, relative_score, opponent_reputation):
    if round_number == 1:
        return 'C'
    if opponent_history[-3:] == ['D', 'D', 'D']:
        return 'N'
    return 'C' if relative_score > 0 else 'D'

strategies = [
    always_cooperate, always_defect, tit_for_tat, score_based_strategy, reputation_based_strategy, nuclear_option_strategy
]
