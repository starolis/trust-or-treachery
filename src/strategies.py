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

def score_based(my_history, opponent_history, round_number, relative_score, opponent_reputation):
    if round_number == 1:
        return 'C'
    if relative_score > 0:
        return 'C'
    return 'D'

def reputation_based(my_history, opponent_history, round_number, relative_score, opponent_reputation):
    if round_number == 1:
        return 'C'
    if opponent_reputation < -10:
        return 'N'
    if relative_score > 0:
        return 'C'
    return 'D'

def nuclear_option(my_history, opponent_history, round_number, relative_score, opponent_reputation):
    if round_number == 1:
        return 'C'
    if opponent_history[-3:] == ['D', 'D', 'D']:
        return 'N'
    return 'C' if relative_score > 0 else 'D'
    
# Additional Strategies
def pattern_exploit(history1, history2, round_number, relative_score, reputation):
    if len(history2) < 3:
        return 'C'
    # Look for patterns in the last three moves of the opponent
    pattern = ''.join(history2[-3:])
    if pattern == 'CCC':
        return 'D'
    elif pattern == 'DDD':
        return 'C'
    else:
        return 'C' if random.random() < 0.5 else 'D'

def sliding_window(history1, history2, round_number, relative_score, reputation):
    if len(history2) < 4:
        return 'C'
    window = history2[-4:]
    coop_count = window.count('C')
    defect_count = window.count('D')
    if coop_count > defect_count:
        return 'C'
    else:
        return 'D'

def wrath(my_history, opponent_history, round_number, relative_score, opponent_reputation):
    if round_number == 1:
        return 'C'
    elif opponent_history.count('D') >= 2:
        return 'D'
    else:
        return opponent_history[-1]


strategies = [
    always_cooperate, always_defect, tit_for_tat, score_based, reputation_based,
    nuclear_option, pattern_exploit, sliding_window, wrath
]
