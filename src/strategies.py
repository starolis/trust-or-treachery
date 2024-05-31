import random


# Example Strategies
def always_cooperate(my_hist, opp_hist, round_num, rel_score, opp_rep):
    return "C"


def always_defect(my_hist, opp_hist, round_num, rel_score, opp_rep):
    return "D"


def tit_for_tat(my_hist, opp_hist, round_num, rel_score, opp_rep):
    if round_num == 1:
        return "C"
    return opp_hist[-1]


def score_based(my_hist, opp_hist, round_num, rel_score, opp_rep):
    if round_num == 1:
        return "C"
    return "C" if rel_score > 0 else "D"


def reputation_based(my_hist, opp_hist, round_num, rel_score, opp_rep):
    if round_num == 1:
        return "C"
    if opp_rep < -10:
        return "N"
    return "C" if rel_score > 0 else "D"


def nuclear_option(my_hist, opp_hist, round_num, rel_score, opp_rep):
    if round_num == 1:
        return "C"
    if opp_hist[-3:] == ["D", "D", "D"]:
        return "N"
    return "C" if rel_score > 0 else "D"


# Additional Strategies
def pattern_exploit(my_hist, opp_hist, round_num, rel_score, opp_rep):
    if len(opp_hist) < 3:
        return "C"
    pattern = "".join(opp_hist[-3:])
    if pattern == "CCC":
        return "D"
    if pattern == "DDD":
        return "C"
    return "C" if random.random() < 0.5 else "D"


def sliding_window(my_hist, opp_hist, round_num, rel_score, opp_rep):
    if len(opp_hist) < 4:
        return "C"
    window = opp_hist[-4:]
    coop_count = window.count("C")
    defect_count = window.count("D")
    return "C" if coop_count > defect_count else "D"


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
]
