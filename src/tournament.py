import random
import time
import openai
from statistics import mean
import numpy as np
from colorama import init, Fore, Style
from strategies2 import strategies

# Initialize colorama
init(autoreset=True)

# Define the initial and advanced payoff matrices
initial_payoff_matrix = {"CC": (3, 3), "CD": (0, 5), "DC": (5, 0), "DD": (1, 1)}
advanced_payoff_matrix = {"CC": (4, 4), "CD": (0, 10), "DC": (10, 0), "DD": (1, 1)}

def get_payoff_matrix(mutual_cooperations):
    return advanced_payoff_matrix if mutual_cooperations >= 100 else initial_payoff_matrix

def add_noise(action, noise_level=0.02):
    noisy = False
    if random.random() < noise_level:
        noisy = True
        action = "D" if action == "C" else "C"
    return action, noisy

def tit_for_tat(history):
    return "C" if len(history) == 0 else history[-1]

def update_reputation(reputation, my_move, opponent_move, expected_move):
    if expected_move == "C" and my_move == "D":
        reputation -= 1
    elif expected_move == "D" and my_move == "C":
        reputation += 1
    return reputation

def play_match(strategy1, strategy2, rounds, initial_reputation1, initial_reputation2, delay=0.1):
    history1, history2 = [], []
    score1, score2 = 0, 0
    reputation1, reputation2 = initial_reputation1, initial_reputation2
    mutual_cooperations = 0
    noise_level = 0.02
    round_history = []
    noise_flags = []

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

        move1, noisy1 = add_noise(move1, noise_level)
        move2, noisy2 = add_noise(move2, noise_level)

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
        round_history.append((move1, move2))
        noise_flags.append((noisy1, noisy2))

    # Print match results
    print(f"\nMatch: {strategy1.__name__} vs {strategy2.__name__}")
    print(f"Rounds Played: {len(round_history)}")
    print(f"Final Score: {strategy1.__name__} = {score1}, {strategy2.__name__} = {score2}")
    print(f"Final Reputation: {strategy1.__name__} = {reputation1}, {strategy2.__name__} = {reputation2}")

    # Format and print round history
    for i in range(0, len(round_history), 50):
        line1 = ""
        line2 = ""
        for j in range(50):
            if i + j < len(round_history):
                move1, move2 = round_history[i + j]
                noisy1, noisy2 = noise_flags[i + j]
                colored_move1 = Fore.GREEN + move1 if move1 == "C" else Fore.RED + move1
                colored_move2 = Fore.GREEN + move2 if move2 == "C" else Fore.RED + move2
                separator1 = " " if not noisy1 else Fore.WHITE + "X"
                separator2 = " " if not noisy2 else Fore.WHITE + "X"
                line1 += f"{colored_move1}{separator1}"
                line2 += f"{colored_move2}{separator2}"
        print(line1)
        print(line2)
        print()

    return score1, score2, reputation1, reputation2

def run_tournament(strategies):
    results = {strategy.__name__: {"score": 0, "reputation": 0, "games": 0} for strategy in strategies}

    for i, strategy1 in enumerate(strategies):
        for j, strategy2 in enumerate(strategies):
            if i < j:  # Ensure each strategy pair is only matched once
                print(f"\nNext Match: {strategy1.__name__} vs {strategy2.__name__}")
                """
                response = input("Play match? (y/n): ").strip().lower()
                if response == 'n':
                    print("Tournament terminated by user.")
                    return results  # Exit the function and terminate the tournament
                """
                rounds = random.randint(195, 205)
                reputation1 = results[strategy1.__name__]["reputation"]
                reputation2 = results[strategy2.__name__]["reputation"]
                score1, score2, new_reputation1, new_reputation2 = play_match(strategy1, strategy2, rounds, reputation1, reputation2, 0.1)
                results[strategy1.__name__]["score"] += score1
                results[strategy1.__name__]["reputation"] += new_reputation1 - reputation1
                results[strategy1.__name__]["games"] += 1
                results[strategy2.__name__]["score"] += score2
                results[strategy2.__name__]["reputation"] += new_reputation2 - reputation2
                results[strategy2.__name__]["games"] += 1

    return results

# Run the tournament
results = run_tournament(strategies)

# Sort the results by score in descending order
sorted_results = sorted(results.items(), key=lambda item: item[1]["score"], reverse=True)

# Print the final results in a clean format
print("\nFinal Tournament Results with Additional Strategies:")
print(f"{'Strategy':<20} {'Total Score':<12} {'Avg Score':<10} {'Reputation':<10} {'Games Played':<12}")
print("=" * 64)
for strategy, data in sorted_results:
    total_score = data["score"]
    games_played = data["games"]
    avg_score = total_score / games_played if games_played > 0 else 0
    reputation = data["reputation"]
    print(f"{strategy:<20} {total_score:<12} {avg_score:<10.2f} {reputation:<10} {games_played:<12}")
