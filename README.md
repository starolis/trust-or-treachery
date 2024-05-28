# Trust or Treachery Tournament

This project is an end-of-year project for implementing strategies in a variant of the prisoner's dilemma game. Students will write Python functions that compete against each other in a tournament to accumulate the highest total score based on a dynamic payoff matrix.

## Project Structure

- `src/`: Contains the Python scripts for the tournament.
  - `tournament.py`: Core tournament logic.
  - `strategies.py`: Example strategies.
- `docs/`: Contains the LaTeX documentation for the project.
- `tests/`: Contains test scripts to ensure the code works as expected.

## How to Run

1. Clone the repository:

   `[git clone https://github.com/starolis/trust-or-treachery.git](https://github.com/starolis/trust-or-treachery.git)`

2. Navigate to the src directory and run the tournament:

   cd trust-or-treachery-tournament/src
   python tournament.py

## Example Strategies

Examples of different strategies are provided in the tournament.py script. These include always_cooperate, always_defect, tit_for_tat, score_based_strategy, reputation_based_strategy, and nuclear_option_strategy.
