import random
from strategies import strategies

# Define the initial and advanced payoff matrices
initial_payoff_matrix = {'CC': (3, 3), 'CD': (0, 5), 'DC': (5, 0), 'DD': (1, 1)}
advanced_payoff_matrix = {'CC': (4, 4), 'CD': (0, 10), 'DC': (10, 0), 'DD': (1, 1)}

def get_payoff_matrix(mutual_cooperations):
    if mutual_cooperations >= 100:
        return advanced_payoff_matrix
    return initial_payoff_matrix

def add_noise(action: str, noise_level: float = 0.02) -> str:
    if random.random() < noise_level:
        return 'D' if action == 'C' else 'C'
    return action

def calculate_reputation(my_history, opponent_history):
    reputation = 0
    for my_move, opponent_move in zip(my_history, opponent_history):
        if my_move == 'C' and opponent_move == 'D':
            reputation -= 1
        elif my_move == 'D' and opponent_move == 'C':
            reputation += 1
    return reputation

def play_match(strategy1, strategy2, rounds):
    history1, history2 = [], []
    score1, score2 = 0, 0
    reputation1, reputation2 = 0, 0
    mutual_cooperations = 0
    noise_level = 0.02

    for round_number in range(1, rounds + 1):
        payoff_matrix = get_payoff_matrix(mutual_cooperations)
        relative_score1 = score1 - score2
        relative_score2 = score2 - score1

        move1 = strategy1(history1, history2, round_number, relative_score1, reputation2)
        move2 = strategy2(history2, history1, round_number, relative_score2, reputation1)

        if move1 == 'N' and move2 == 'N':
            break
        elif move1 == 'N':
            reputation1 += 5
            reputation2 -= 5
            break
        elif move2 == 'N':
            reputation2 += 5
            reputation1 -= 5
            break

        move1 = add_noise(move1, noise_level)
        move2 = add_noise(move2, noise_level)

        outcome = move1 + move2
        if outcome == 'CC':
            mutual_cooperations += 1
        score1 += payoff_matrix[outcome][0]
        score2 += payoff_matrix[outcome][1]

        history1.append(move1)
        history2.append(move2)

        reputation1 = calculate_reputation(history1, history2)
        reputation2 = calculate_reputation(history2, history1)

    return score1, score2, reputation1, reputation2

def run_tournament(strategies):
    results = {strategy.__name__: {'score': 0, 'reputation': 0} for strategy in strategies}

    for i, strategy1 in enumerate(strategies):
        for j, strategy2 in enumerate(strategies):
            if i != j:
                rounds = random.randint(195, 205)
                score1, score2, reputation1, reputation2 = play_match(strategy1, strategy2, rounds)
                results[strategy1.__name__]['score'] += score1
                results[strategy1.__name__]['reputation'] = reputation1
                results[strategy2.__name__]['score'] += score2
                results[strategy2.__name__]['reputation'] = reputation2

    return results

# Example Strategies
def always_cooperate(my_history, opponent_history, round_number, my_score, opponent_score):
    return 'C'

def always_defect(my_history, opponent_history, round_number, my_score, opponent_score):
    return 'D'

def tit_for_tat(my_history, opponent_history, round_number, my_score, opponent_score):
    if round_number == 1:
        return 'C'
    else:
        return opponent_history[-1]

def random_50(my_history, opponent_history, round_number, my_score, opponent_score):
    if random.random() > 0.5:
        return 'C'
    else:
        return 'D'

def random_90(my_history, opponent_history, round_number, my_score, opponent_score):
    if random.random() > 0.9:
        return 'C'
    else:
        return 'D'

def random_10(my_history, opponent_history, round_number, my_score, opponent_score):
    if random.random() > 0.1:
        return 'C'
    else:
        return 'D'

def grim_trigger(my_history, opponent_history, round_number, my_score, opponent_score):
    if 'D' in opponent_history:
        return 'D'
    return 'C'

def pavlov(my_history, opponent_history, round_number, my_score, opponent_score):
    if round_number == 1:
        return 'C'
    if my_history[-1] == opponent_history[-1]:
        return my_history[-1]
    return 'C' if my_history[-1] == 'D' else 'D'

def random_70(my_history, opponent_history, round_number, my_score, opponent_score):
    return 'C' if random.random() < 0.7 else 'D'

def tit_for_two_tats(my_history, opponent_history, round_number, my_score, opponent_score):
    if round_number == 1:
        return 'C'
    if len(opponent_history) >= 2 and opponent_history[-1] == 'D' and opponent_history[-2] == 'D':
        return 'D'
    return 'C'

def generous_tit_for_tat(my_history, opponent_history, round_number, my_score, opponent_score):
    if round_number == 1:
        return 'C'
    if opponent_history[-1] == 'D' and random.random() > 0.1:  # 10% chance to forgive
        return 'D'
    return 'C'

def adaptive_strategy(my_history, opponent_history, round_number, my_score, opponent_score):
    if round_number == 1:
        return 'C'
    cooperation_rate = opponent_history.count('C') / len(opponent_history)
    if cooperation_rate > 0.5:
        return 'C'
    return 'D'

def win_stay_lose_shift(my_history, opponent_history, round_number, my_score, opponent_score):
    if round_number == 1:
        return 'C'
    if my_history[-1] == opponent_history[-1]:
        return my_history[-1]
    return 'C' if my_history[-1] == 'D' else 'D'

def prober(my_history, opponent_history, round_number, my_score, opponent_score):
    if round_number < 3:
        return 'D'
    if round_number == 3:
        return 'C'
    return tit_for_tat(my_history, opponent_history, round_number, my_score, opponent_score)

def adaptive_tit_for_tat_with_occasional_defection(my_history, opponent_history, round_number, my_score, opponent_score):
    if round_number == 1:
        return 'C'
    if opponent_history[-1] == 'D':
        return 'D'
    if round_number % 10 == 0:  # Occasionally defect every 10 rounds
        return 'D'
    return 'C'

def dynamic_hysteresis(my_history, opponent_history, round_number, my_score, opponent_score, memory=10):
    if round_number == 1:
        dynamic_hysteresis.memory = {}  # Initialize the memory dictionary
        return 'C'
    
    # Create a key based on the last `memory` moves of both players
    key = (tuple(my_history[-memory:]), tuple(opponent_history[-memory:]))
    
    # Check if the key exists in the memory
    if key in dynamic_hysteresis.memory:
        return dynamic_hysteresis.memory[key]
    
    # Default to Tit for Tat if the key is not found
    return opponent_history[-1]

def score_based_tit_for_tat(my_history, opponent_history, round_number, my_score, opponent_score):
    if round_number == 1:
        return 'C'
    if my_score > opponent_score:
        return 'C'
    return opponent_history[-1]

def score_based_generous_tit_for_tat(my_history, opponent_history, round_number, my_score, opponent_score):
    if round_number == 1:
        return 'C'
    if opponent_history[-1] == 'D':
        if my_score > opponent_score and random.random() > 0.2:  # 20% chance to forgive if leading
            return 'C'
        return 'D'
    return 'C'

def score_based_adaptive_strategy(my_history, opponent_history, round_number, my_score, opponent_score):
    if round_number == 1:
        return 'C'
    cooperation_rate = opponent_history.count('C') / len(opponent_history)
    if cooperation_rate > 0.5 and my_score >= opponent_score:
        return 'C'
    return 'D'

# Add the new strategy to the list of strategies
strategies = [
    always_cooperate, always_defect, tit_for_tat, random_50, random_90, random_10, grim_trigger, pavlov, random_70,
    tit_for_two_tats, generous_tit_for_tat, adaptive_strategy, win_stay_lose_shift, prober, adaptive_tit_for_tat_with_occasional_defection,
    dynamic_hysteresis, score_based_tit_for_tat, score_based_generous_tit_for_tat, score_based_adaptive_strategy
]

# Run the tournament
results = run_tournament(strategies)

# Sort the results by score in descending order
sorted_results = sorted(results.items(), key=lambda item: item[1], reverse=True)

# Print the results
for strategy, score in sorted_results:
    print(f"{strategy}: {score}")