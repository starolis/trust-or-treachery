import random


def always_cooperate(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    return "C"


def always_defect(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    return "D"


def tit_for_tat(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    if round_number == 1:
        return "C"
    return opponent_history[-1]


def double_whammy(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    if round_number == 1:
        return "C"  # Always cooperate on the first round

    # Check if in the defecting period after opponent's defect
    if round_number > 1:
        last_opponent_move = opponent_history[-1]

        if round_number == 2:
            if last_opponent_move == "D":
                return "D"
            else:
                return "C"

        if last_opponent_move == "D":
            if len(opponent_history) >= 2 and opponent_history[-2] == "D":
                return "D"
            else:
                return "D"
        else:
            if opponent_history[-2] == "D":
                return "D"
            else:
                return "C"


def exotic_potato(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    if round_number == 1:
        return "C"
    if opponent_history[-1] == "C":
        return "C"
    return "D" if random.random() < 0.98 else "C"


def tombuck_tim(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    # Always defect on the first round
    if round_number == 1:
        return "D"
    # Cooperate if the opponent cooperated in the last round
    elif opponent_history[-1] == "C":
        return "C"
    # Otherwise, defect with a 90% chance, cooperate 10% of the time
    return "D" if random.random() < 0.9 else "C"


def majic_eight_ball(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    if len(opponent_history) < 8:
        return "C"
    window = opponent_history[-8:]
    coop_count = window.count("C")
    defect_count = window.count("D")
    return "C" if coop_count > defect_count else "D"


def adaptive_randomization(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    # Initialize the first move to cooperation
    if round_number == 1:
        return "C"
        # Randomly decide to add some noise to the strategy
    noise_threshold = 0.1  # 10% chance to randomize the move
    if random.random() < noise_threshold:
        return random.choice(["C", "D"])

    # Analyze the opponent's last three moves
    recent_opponent_moves = opponent_history[-3:]

    # Determine the opponent's tendency based on their last three moves
    opponent_cooperation_rate = recent_opponent_moves.count("C") / 3

    # If the opponent has cooperated at least twice in the last three moves, cooperate
    if opponent_cooperation_rate >= 2 / 3:
        return "C"

    # If the opponent has defected at least twice in the last three moves, defect
    if opponent_cooperation_rate <= 1 / 3:
        return "D"

    # In other cases, use a mixed strategy based on the relative score
    # If we are ahead in score, tend to cooperate more
    if relative_score > 0:
        return "C" if random.random() < 0.7 else "D"
    # If we are behind in score, tend to defect more
    else:
        return "D" if random.random() < 0.7 else "C"


def wrath(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    if round_number == 1:
        return "C"
    elif opponent_history.count("D") >= 2:
        return "D"
    else:
        return opponent_history[-1]
