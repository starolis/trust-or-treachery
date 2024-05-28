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

# Run the tournament
results = run_tournament(strategies)

# Sort the results by score in descending order
sorted_results = sorted(results.items(), key=lambda item: item[1]['score'], reverse=True)
# Print the results
for strategy, score in sorted_results:
    print(f"{strategy}: {score}")