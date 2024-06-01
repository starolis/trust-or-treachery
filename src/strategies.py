import random


# Example Strategies
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


def score_based(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    if round_number == 1:
        return "C"
    return "C" if relative_score > 0 else "D"


def reputation_based(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    if round_number == 1:
        return "C"
    if opponent_reputation < -10:
        return "N"
    return "C" if relative_score > 0 else "D"


def nuclear_option(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    if round_number == 1:
        return "C"
    if opponent_history[-3:] == ["D", "D", "D"]:
        return "N"
    return "C" if relative_score > 0 else "D"


# Additional Strategies
def pattern_exploit(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    if len(opponent_history) < 3:
        return "C"
    pattern = "".join(opponent_history[-3:])
    if pattern == "CCC":
        return "D"
    if pattern == "DDD":
        return "C"
    return "C" if random.random() < 0.5 else "D"


def sliding_window(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    if len(opponent_history) < 4:
        return "C"
    window = opponent_history[-4:]
    coop_count = window.count("C")
    defect_count = window.count("D")
    return "C" if coop_count > defect_count else "D"


def sliding_five(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    if len(opponent_history) < 5:
        return "C"
    window = opponent_history[-5:]
    coop_count = window.count("C")
    defect_count = window.count("D")
    return "C" if coop_count > defect_count else "D"


def sliding_six(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    if len(opponent_history) < 6:
        return "C"
    window = opponent_history[-6:]
    coop_count = window.count("C")
    defect_count = window.count("D")
    return "C" if coop_count > defect_count else "D"


def sliding_seven(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    if len(opponent_history) < 7:
        return "C"
    window = opponent_history[-7:]
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


def sliding_nuke(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    if len(opponent_history) < 4:
        return "C"
    if len(opponent_history) > 193:
        return "N"
    window = opponent_history[-4:]
    coop_count = window.count("C")
    defect_count = window.count("D")
    return "C" if coop_count > defect_count else "D"


# Grudger strategy
def grudger(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    if "D" in opponent_history:
        return "D"
    return "C"


# Random strategy
def random_strategy(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    return "C" if random.random() < 0.5 else "D"


# Pavlov strategy
def pavlov(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    if round_number == 1:
        return "C"
    last_round = my_history[-1] + opponent_history[-1]
    if last_round in ["CC", "DD"]:
        return "C"
    return "D"


# Forgiving Tit-for-Tat strategy
def forgiving_tit_for_tat(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    if round_number == 1:
        return "C"
    if opponent_history[-1] == "D" and "D" in opponent_history[-3:]:
        return "D"
    return "C"


# Adaptive strategy
def adaptive(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    if round_number == 1:
        return "C"
    defect_rate = opponent_history.count("D") / len(opponent_history)
    if defect_rate > 0.3:
        return "D"
    return "C"


def probing_defector(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    if round_number <= 2:
        return "C"
    if round_number % 3 == 0:
        return "D"
    return "C"


def calculated_reciprocity(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    if round_number == 1:
        return "C"
    defect_rate = opponent_history.count("D") / len(opponent_history)
    if defect_rate > 0.5:
        return "D"
    return "C"


def fair_weather_friend(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    if relative_score > 0:
        return "C"
    return "D"


def punisher(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    if round_number == 1:
        return "C"
    if opponent_history[-1] == "D":
        return "D"
    if "D" in opponent_history[-3:]:
        return "D"
    return "C"


def mimic_after_two_defects(
    my_history, opponent_history, round_number, relative_score, opponent_reputation
):
    if round_number == 1:
        return "C"
    if "DD" in "".join(opponent_history):
        return opponent_history[-1]
    return "C"

# List of strategies
strategies = [
    always_cooperate,
    always_defect,
    tit_for_tat,
    score_based,
    reputation_based,
    nuclear_option,
    pattern_exploit,
    sliding_window,
    #    sliding_five,
    #    sliding_six,
    #    sliding_seven,
    sliding_eight,
    #    sliding_nine,
    #    sliding_nuke,
    grudger,
    random_strategy,
    pavlov,
    forgiving_tit_for_tat,
    adaptive,
    probing_defector,
    calculated_reciprocity,
    fair_weather_friend,
    punisher,
    mimic_after_two_defects
]
