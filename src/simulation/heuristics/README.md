# N-Queens Heuristic Analysis

This program analyzes an N-Queens problem solver that **heuristically employs an Iterative Repair method**. It evaluates the solver across various board sizes, collecting data on execution time, number of steps, and success rate. This data is then saved to a CSV file and visualized in diagrams.

The script (`analyze_n_queens.py`) does the following:
1. Runs the N-Queens problem-solving algorithm, which uses an **Iterative Repair method**, for a specified number of iterations across different N (board size) values.
2. For each N size, it performs 25 runs with different random number generator seeds.
3. Records the execution time, the number of steps required for a solution (if successful), and whether the solution was successful.
4. Saves the aggregated results to a CSV file and generates diagrams visualizing key performance metrics such as average execution time, average steps for solved instances, and success rate against board size.

## Generated Diagrams

The analysis script generates the following diagrams:

### Average Execution Time vs. Board Size
This diagram shows how the average time required to solve the N-Queens problem changes with the increase in board size (N).

![Average Execution Time](https://apagyidavid.web.elte.hu/2024-2025-2/heuristics/results/n_queens/n_queens_avg_time.svg)

### Average Steps (Solved Cases) vs. Board Size
This diagram illustrates the average number of steps required to find a solution in successfully solved cases, as a function of board size (N).

![Average Steps](https://apagyidavid.web.elte.hu/2024-2025-2/heuristics/results/n_queens/n_queens_avg_steps.svg)

### Success Rate vs. Board Size
This diagram shows the solution success rate in percentage, as the board size (N) increases. In all tested board sizes for this analysis, the program successfully found a solution for every run.

![Success Rate](https://apagyidavid.web.elte.hu/2024-2025-2/heuristics/results/n_queens/n_queens_success_rate.svg)

### Raw Simulation Data
The raw data from the simulations, including individual run times, step counts, and success status for each seed and board size, is available in a CSV file.

[Download Raw Simulation Data (n_queens_analysis.csv)](https://apagyidavid.web.elte.hu/2024-2025-2/heuristics/results/n_queens/n_queens_analysis.csv)
