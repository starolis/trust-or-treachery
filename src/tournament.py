import random
from statistics import mean
import numpy as np
from colorama import init, Fore, Style
from strategies import strategies

# Initialize colorama
init(autoreset=True)

# Define the initial and advanced payoff matrices
initial_payoff_matrix = {"CC": (3, 3), "CD": (0, 5), "DC": (5, 0), "DD": (1, 1)}
advanced_payoff_matrix = {"CC": (4, 4), "CD": (0, 10), "DC": (10, 0), "DD": (1, 1)}

def get_payoff_matrix(mutual_cooperations):
    return advanced_payoff_matrix if mutual_cooperations >= 100 else initial_payoff_matrix

def add_noise(action, noise_level=0.02):
    if random.random() < noise_level:
        return "D" if action == "C" else "C"
    return action

def tit_for_tat(history):
    return "C" if len(history) == 0 else history[-1]

def update_reputation(reputation, my_move, opponent_move, expected_move):
    if expected_move == "C" and my_move == "D":
        reputation -= 1
    elif expected_move == "D" and my_move == "C":
        reputation += 1
    return reputation

def play_match(strategy1, strategy2, rounds, initial_reputation1, initial_reputation2):
    history1, history2 = [], []
    score1, score2 = 0, 0
    reputation1, reputation2 = initial_reputation1, initial_reputation2
    mutual_cooperations = 0
    noise_level = 0.02

    for round_number in range(1, rounds + 1):
        payoff_matrix = get_payoff_matrix(mutual_cooperations)
        relative_score1 = score1 - score2
        relative_score2 = score2 - score1

        move1 = strategy1(history1, history2, round_number, relative_score1, reputation2)
        move2 = strategy2(history2, history1, round_number, relative_score2, reputation1)

        if move1 == "N" and move2 == "N":
            break
        elif move1 == "N":
            reputation1 += 5
            reputation2 -= 5
            break
        elif move2 == "N":
            reputation2 += 5
            reputation1 -= 5
            break

        move1 = add_noise(move1, noise_level)
        move2 = add_noise(move2, noise_level)

        outcome = move1 + move2
        if outcome == "CC":
            mutual_cooperations += 1
        score1 += payoff_matrix[outcome][0]
        score2 += payoff_matrix[outcome][1]

        expected_move1 = tit_for_tat(history2)
        expected_move2 = tit_for_tat(history1)
        reputation1 = update_reputation(reputation1, move1, move2, expected_move1)
        reputation2 = update_reputation(reputation2, move2, move1, expected_move2)

        history1.append(move1)
        history2.append(move2)

    return score1, score2, reputation1, reputation2

def run_tournament(strategies):
    results = {strategy.__name__: {"score": 0, "reputation": 0, "games": 0} for strategy in strategies}

    for i, strategy1 in enumerate(strategies):
        for j, strategy2 in enumerate(strategies):
            if i < j:  # Ensure each strategy pair is only matched once
                rounds = random.randint(195, 205)
                reputation1 = results[strategy1.__name__]["reputation"]
                reputation2 = results[strategy2.__name__]["reputation"]
                score1, score2, new_reputation1, new_reputation2 = play_match(strategy1, strategy2, rounds, reputation1, reputation2)
                results[strategy1.__name__]["score"] += score1
                results[strategy1.__name__]["reputation"] += new_reputation1 - reputation1
                results[strategy1.__name__]["games"] += 1
                results[strategy2.__name__]["score"] += score2
                results[strategy2.__name__]["reputation"] += new_reputation2 - reputation2
                results[strategy2.__name__]["games"] += 1

    return results

def run_multiple_tournaments(num_runs, strategies):
    accumulated_results = {strategy.__name__: {"score": [], "reputation": [], "games": []} for strategy in strategies}

    for _ in range(num_runs):
        results = run_tournament(strategies)
        for strategy, data in results.items():
            accumulated_results[strategy]["score"].append(data["score"])
            accumulated_results[strategy]["reputation"].append(data["reputation"])
            accumulated_results[strategy]["games"].append(data["games"])

    # Calculate the average results using NumPy for performance
    average_results = {}
    for strategy, data in accumulated_results.items():
        average_results[strategy] = {
            "score": np.mean(data["score"]),
            "reputation": np.mean(data["reputation"]),
            "games": np.mean(data["games"]),
        }

    return average_results

# Run the tournament 100 times and accumulate results
num_runs = 100
average_results = run_multiple_tournaments(num_runs, strategies)

# Sort the results by average score in descending order
sorted_average_results = sorted(average_results.items(), key=lambda item: item[1]["score"], reverse=True)

# Print the average results in a clean format
print("\nAverage Tournament Results over 100 Runs:")
print(f"{'Strategy':<20} {'Avg Score':<10} {'Avg Reputation':<15} {'Avg Games Played':<17}")
print("=" * 62)
for strategy, data in sorted_average_results:
    avg_score = data["score"]
    avg_reputation = data["reputation"]
    avg_games_played = data["games"]
    print(f"{strategy:<20} {avg_score:<10.2f} {avg_reputation:<15.2f} {avg_games_played:<17.2f}")
