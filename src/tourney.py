import random
import time
import openai
import os
from statistics import mean
import numpy as np
from colorama import init, Fore, Style
from entrants import strategies
from dotenv import load_dotenv
import textwrap

# Load API key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize colorama
init(autoreset=True)

# Define the initial and advanced payoff matrices
initial_payoff_matrix = {"CC": (3, 3), "CD": (0, 5), "DC": (5, 0), "DD": (1, 1)}
advanced_payoff_matrix = {"CC": (4, 4), "CD": (0, 10), "DC": (10, 0), "DD": (1, 1)}


def get_payoff_matrix(mutual_cooperations):
    return (
        advanced_payoff_matrix if mutual_cooperations >= 100 else initial_payoff_matrix
    )


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


def wrap_text(text, width=100):
    return "\n".join(textwrap.wrap(text, width))


def play_match(
    strategy1, strategy2, rounds, initial_reputation1, initial_reputation2, delay=0.1
):
    history1, history2 = [], []
    score1, score2 = 0, 0
    reputation1, reputation2 = initial_reputation1, initial_reputation2
    mutual_cooperations = 0
    noise_level = 0.05
    round_history = []
    noise_flags = []

    for round_number in range(1, rounds + 1):
        payoff_matrix = get_payoff_matrix(mutual_cooperations)
        relative_score1 = score1 - score2
        relative_score2 = score2 - score1

        move1 = strategy1(
            history1, history2, round_number, relative_score1, reputation2
        )
        move2 = strategy2(
            history2, history1, round_number, relative_score2, reputation1
        )

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
    print(
        f"Final Score: {strategy1.__name__} = {score1}, {strategy2.__name__} = {score2}"
    )
    print(
        f"Final Reputation: {strategy1.__name__} = {reputation1}, {strategy2.__name__} = {reputation2}"
    )

    # Format and print round history
    for i in range(0, len(round_history), 52):
        line1 = ""
        line2 = ""
        for j in range(52):
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

    return score1, score2, reputation1, reputation2, round_history


def generate_commentary(strategy1_name, strategy2_name, score1, score2, round_history):
    prompt = (
        f"Analyze the following match as if it were a sporting event. Provide a dramatic commentary within 100 words.\n\n"
        f"Match: {strategy1_name} vs {strategy2_name}\n"
        f"Final Score: {strategy1_name} = {score1}, {strategy2_name} = {score2}\n"
        f"Round History: {round_history}\n\n"
        f"Commentary:"
    )

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a witty and humorous commentator providing in-depth analysis of a tournament.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=200,  # Slightly reduced max tokens to leave some buffer
        temperature=0.7,
    )

    return wrap_text(response.choices[0].message.content.strip())


def generate_final_commentary(sorted_results):
    prompt = "Provide a final commentary on the overall tournament and the ranking of competitors in 300 words or less. Here are the final results:\n\n"
    for strategy, data in sorted_results:
        total_score = data["score"]
        games_played = data["games"]
        avg_score = total_score / games_played if games_played > 0 else 0
        reputation = data["reputation"]
        prompt += (
            f"{strategy}: Total Score = {total_score}, Avg Score = {avg_score:.2f}, "
            f"Reputation = {reputation}, Games Played = {games_played}\n"
        )
    prompt += "\nFinal Commentary:"

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a witty and humorous commentator providing in-depth analysis of a tournament.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=500,
        temperature=0.7,
    )

    return wrap_text(response.choices[0].message.content.strip())


def run_tournament(strategies):
    results = {
        strategy.__name__: {"score": 0, "reputation": 0, "games": 0}
        for strategy in strategies
    }

    # Create a list of all possible strategy matchups
    matchups = [
        (strategies[i], strategies[j])
        for i in range(len(strategies))
        for j in range(i + 1, len(strategies))
    ]

    # Shuffle the list to randomize the order
    random.shuffle(matchups)

    commentary_enabled = True
    skip_prompt = False

    for strategy1, strategy2 in matchups:
        print(f"\nNext Match: {strategy1.__name__} vs {strategy2.__name__}")

        if not skip_prompt:
            print("Options:")
            print("1) Proceed to the next match and perform commentary")
            print("2) Proceed to the next match and do not perform commentary")
            print(
                "3) Run the tournament to completion without commentary or further prompting between matches"
            )
            print("4) Stop the tournament and display the results")
            choice = input("Enter your choice (1-4): ").strip()

            if choice == "1":
                commentary_enabled = True
            elif choice == "2":
                commentary_enabled = False
            elif choice == "3":
                commentary_enabled = False
                skip_prompt = True
            elif choice == "4":
                print("Tournament terminated by user.")
                return results  # Exit the function and terminate the tournament
            else:
                print("Invalid choice. Please enter 1, 2, 3, or 4.")
                continue

        rounds = random.randint(195, 205)
        reputation1 = results[strategy1.__name__]["reputation"]
        reputation2 = results[strategy2.__name__]["reputation"]
        score1, score2, new_reputation1, new_reputation2, round_history = play_match(
            strategy1, strategy2, rounds, reputation1, reputation2, 0.1
        )
        results[strategy1.__name__]["score"] += score1
        results[strategy1.__name__]["reputation"] += new_reputation1 - reputation1
        results[strategy1.__name__]["games"] += 1
        results[strategy2.__name__]["score"] += score2
        results[strategy2.__name__]["reputation"] += new_reputation2 - reputation2
        results[strategy2.__name__]["games"] += 1

        if commentary_enabled and not skip_prompt:
            commentary = generate_commentary(
                strategy1.__name__, strategy2.__name__, score1, score2, round_history
            )
            print(f"\nGPT Commentary:\n{commentary}\n")

    return results


# Run the tournament
results = run_tournament(strategies)

# Sort the results by score in descending order
sorted_results = sorted(
    results.items(), key=lambda item: item[1]["score"], reverse=True
)

# Print the final results in a clean format
print("\nFinal Tournament Results with Additional Strategies:")
print(
    f"{'Strategy':<20} {'Total Score':<12} {'Avg Score':<10} {'Reputation':<10} {'Games Played':<12}"
)
print("=" * 64)
for strategy, data in sorted_results:
    total_score = data["score"]
    games_played = data["games"]
    avg_score = total_score / games_played if games_played > 0 else 0
    reputation = data["reputation"]
    print(
        f"{strategy:<20} {total_score:<12} {avg_score:<10.2f} {reputation:<10} {games_played:<12}"
    )

# Generate final tournament commentary
final_commentary = generate_final_commentary(sorted_results)
print(f"\nGPT Final Commentary:\n{final_commentary}\n")
