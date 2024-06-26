import random

# Payoffs
R = 3  # Reward
P = 1  # Punishment
T = 5  # Temptation
S = 0  # Sucker


# Strategy implementations
def unconditional_cooperator(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    return "C"


def unconditional_defector(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    return "D"


def random_strategy(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    return "C" if random.random() < 0.5 else "D"


def probability_p_cooperator_75(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    p = 0.75
    return "C" if random.random() < p else "D"


def tit_for_tat(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    if round_number == 1:
        return "C"
    return opponent_history[-1]


def suspicious_tit_for_tat(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    if round_number == 1:
        return "D"
    return opponent_history[-1]


def generous_tit_for_tat(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    def g(R, P, T, S):
        return min(1 - (T - R) / (R - S), (R - P) / (T - P))

    if round_number == 1:
        return "C"
    if opponent_history[-1] == "D" and random.random() < g(R, P, T, S):
        return "C"
    return opponent_history[-1]


def gradual_tit_for_tat(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    if round_number == 1:
        return "C"
    if opponent_history[-1] == "D":
        return "D"
    if "D" in opponent_history[-2:]:
        return "C"
    return "C"


def imperfect_tit_for_tat(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    if round_number == 1:
        return "C"
    if random.random() < 0.9:
        return opponent_history[-1]
    return "D" if opponent_history[-1] == "C" else "C"


def tit_for_two_tats(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    if round_number == 1:
        return "C"
    if (
        len(opponent_history) >= 2
        and opponent_history[-1] == "D"
        and opponent_history[-2] == "D"
    ):
        return "D"
    return "C"


def two_tits_for_tat(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    if round_number == 1:
        return "C"
    if opponent_history[-1] == "D":
        return "D"
    if "D" in opponent_history[-2:]:
        return "D"
    return "C"


def omega_tit_for_tat(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    def deadlock_or_randomness(opponent_history):
        # Placeholder for actual deadlock or randomness calculation
        return False, False

    if round_number == 1:
        return "C"
    deadlock, randomness = deadlock_or_randomness(opponent_history)
    if deadlock:
        return "C"
    if randomness:
        return "D"
    return opponent_history[-1]


def grim_trigger(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    if "D" in opponent_history:
        return "D"
    return "C"


def discriminating_altruist(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    if "D" not in opponent_history:
        return "C"
    return "N"


def pavlov(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    if round_number == 1:
        return "C"
    last_round = my_history[-1] + opponent_history[-1]
    if last_round in ["CC", "DD"]:
        return "C"
    return "D"


def n_pavlov_2(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    n = 2
    if round_number == 1:
        return "C"
    p = 1 / n
    last_payoff = {"CC": R, "CD": S, "DC": T, "DD": P}[
        my_history[-1] + opponent_history[-1]
    ]
    if last_payoff == R:
        return "C" if random.random() < min(1, p + 1 / n) else "D"
    if last_payoff == P:
        return "C" if random.random() < max(0, p - 1 / n) else "D"
    if last_payoff == T:
        return "C" if random.random() < min(1, p + 2 / n) else "D"
    if last_payoff == S:
        return "C" if random.random() < max(0, p - 2 / n) else "D"


def adaptive_pavlov(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    if round_number <= 6:
        return tit_for_tat(
            my_history,
            opponent_history,
            round_number,
            relative_score,
            opponent_reputation,
        )
    # Placeholder for actual adaptive strategy based on opponent categorization
    return pavlov(
        my_history, opponent_history, round_number, relative_score, opponent_reputation
    )


def reactive_50_50_50(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    y, p, q = 0.5, 0.5, 0.5
    if round_number == 1:
        return "C" if random.random() < y else "D"
    if opponent_history[-1] == "C":
        return "C" if random.random() < p else "D"
    return "C" if random.random() < q else "D"


def memory_one_50_50_50_50(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    p, q, r, s = 0.5, 0.5, 0.5, 0.5
    if round_number == 1:
        return "C" if random.random() < p else "D"
    last_move = my_history[-1] + opponent_history[-1]
    if last_move == "CC":
        return "C" if random.random() < p else "D"
    if last_move == "CD":
        return "C" if random.random() < q else "D"
    if last_move == "DC":
        return "C" if random.random() < r else "D"
    if last_move == "DD":
        return "C" if random.random() < s else "D"


def zero_determinant(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    # Placeholder for actual Zero Determinant strategy
    return "C" if random.random() < 0.5 else "D"


def equalizer_2(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    # Placeholder for actual Equalizer strategy
    return "C" if random.random() < 0.75 else "D"


def extortionary_2(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    # Placeholder for actual Extortionary strategy
    return "C" if random.random() < 0.875 else "D"


def generous_2(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    # Placeholder for actual Generous strategy
    return "C" if random.random() < 1 else "D"


def good_strategy(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    # Placeholder for actual Good strategy
    return "C" if random.random() < 0.5 else "D"


# Sliding strategies
def sliding_three(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    if len(opponent_history) < 3:
        return "C"
    window = opponent_history[-3:]
    coop_count = window.count("C")
    defect_count = window.count("D")
    return "C" if coop_count > defect_count else "D"


def sliding_eight(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    if len(opponent_history) < 8:
        return "C"
    window = opponent_history[-8:]
    coop_count = window.count("C")
    defect_count = window.count("D")
    return "C" if coop_count > defect_count else "D"


def sliding_nine(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    if len(opponent_history) < 9:
        return "C"
    window = opponent_history[-9:]
    coop_count = window.count("C")
    defect_count = window.count("D")
    return "C" if coop_count > defect_count else "D"

def sliding_fifteen(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    if len(opponent_history) < 15:
        return "C"
    window = opponent_history[-15:]
    coop_count = window.count("C")
    defect_count = window.count("D")
    return "C" if coop_count > defect_count else "D"


def sliding_sixteen(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    if len(opponent_history) < 16:
        return "C"
    window = opponent_history[-16:]
    coop_count = window.count("C")
    defect_count = window.count("D")
    return "C" if coop_count > defect_count else "D"


def sliding_thirty_two(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    if len(opponent_history) < 32:
        return "C"
    window = opponent_history[-32:]
    coop_count = window.count("C")
    defect_count = window.count("D")
    return "C" if coop_count > defect_count else "D"


def exploiter_of_magic(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    # Defect three out of every eight rounds
    cycle_position = (round_number - 1) % 8
    if cycle_position in [0, 1, 2, 3, 4]:
        return "C"
    return "D"


def selective_memory(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    window_size = 8
    if round_number <= window_size:
        return "C"  # Start with cooperation in the initial rounds

    # Create weights for the last 10 moves, most recent move gets the highest weight
    weights = list(range(1, window_size + 1))

    # Extract the last 10 moves from opponent history
    recent_moves = opponent_history[-window_size:]

    # Calculate weighted counts of cooperation and defection
    weighted_coop = sum(w for move, w in zip(recent_moves, weights) if move == "C")
    weighted_defect = sum(w for move, w in zip(recent_moves, weights) if move == "D")

    # Decide the next move based on the weighted counts
    return "C" if weighted_coop > weighted_defect else "D"


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


def tombuck_tim(my_history, opponent_history, round_number, relative_score, opponent_reputation):
    # Always defect on the first round
    if round_number == 1:
        return "D"
    # Cooperate if the opponent cooperated in the last round
    elif opponent_history[-1] == "C":
        return "C"
    # Otherwise, defect with a 90% chance, cooperate 10% of the time
    return "D" if random.random() < 0.9 else "C"


def james_strat(
    history, opponent_history, round_number, relative_score, opponent_reputation
):
    rounds_remaining = 195 - round_number
    predefined_moves = ["C", "D", "C", "C", "D", "D", "C", "D", "C", "D"]

    if round_number <= 10:
        return predefined_moves[round_number - 1]

    opponent_cooperates = opponent_history.count("C")
    opponent_defects = opponent_history.count("D")
    total_moves = len(opponent_history)

    always_betray = opponent_defects == total_moves
    always_cooperate = opponent_cooperates == total_moves

    if opponent_history[-1] == "D":
        likely_tit_for_tat = opponent_history[-2:] == ["C", "D"]
    else:
        likely_tit_for_tat = False

    if always_cooperate:
        return "D" if rounds_remaining <= 5 else "C"
    elif always_betray:
        return "D"
    elif likely_tit_for_tat:
        return "C" if opponent_history[-1] == "C" else "D"
    else:
        return "C" if opponent_history[-1] == "C" else "D"

def salty_tit_for_tat(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    # First move is cooperate
    if round_number == 1:
        return "C"

    # Handle the three-move sequence
    if len(my_history) >= 3:
        if my_history[-3:] == ["D", "D", "C"]:
            # Sequence complete, now revert to tit-for-tat
            if opponent_history[-1] == "D":
                return "D"
            else:
                return "C"
        elif my_history[-2:] == ["D", "D"]:
            return "C"
        elif my_history[-1] == "D":
            return "D"

    # If the opponent defected in the last round, start the sequence
    if opponent_history[-1] == "D":
        return "D"
    else:
        return "C"


# List of strategies
strategies = [
    sliding_eight,
    james_strat,
    unconditional_cooperator,
    unconditional_defector,
    random_strategy,
    probability_p_cooperator_75,
    tit_for_tat,
    suspicious_tit_for_tat,
    generous_tit_for_tat,
    gradual_tit_for_tat,
    imperfect_tit_for_tat,
    tit_for_two_tats,
    two_tits_for_tat,
    omega_tit_for_tat,
    grim_trigger,
    discriminating_altruist,
    pavlov,
    n_pavlov_2,
    adaptive_pavlov,
    reactive_50_50_50,
    memory_one_50_50_50_50,
    extortionary_2,
    generous_2,
    good_strategy,
    sliding_three,
    sliding_thirty_two,
    exploiter_of_magic,
    selective_memory,
]
