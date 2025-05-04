import logging
import time
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from simulation.heuristics.n_queens import Chessboard, Solver, SolverStatus

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def run_analysis(output_dir: Path, num_iterations: int = 100, runs_per_size: int = 10):
    """Run N-Queens solver analysis for various sizes and save results."""
    output_dir.mkdir(parents=True, exist_ok=True)
    results_file = output_dir / "n_queens_analysis.csv"
    results_list = []

    logger.info(f"Starting N-Queens analysis. Results will be saved to {results_file}")

    for k in range(num_iterations):
        n = 100 + k * 100
        max_steps = n * 100
        solved_count = 0
        total_steps = 0
        total_time = 0.0

        logger.info(f"Analyzing board size: {n} (k={k})")

        for run in range(runs_per_size):
            seed = k * runs_per_size + run
            start_time = time.perf_counter()
            solved = False
            steps = max_steps

            try:
                board = Chessboard.from_random_permutation(n, seed=seed)
                solver = Solver(board, max_steps=max_steps)
                solver.solve()
                if solver.status == SolverStatus.SOLVED:
                    solved = True
                    steps = solver.current_step
                    solved_count += 1
                    total_steps += steps
            except RuntimeError:
                logger.warning(f"  Run {run + 1}/{runs_per_size} (seed={seed}) failed: Max steps reached.")
                steps = max_steps

            end_time = time.perf_counter()
            run_time = end_time - start_time
            total_time += run_time

            results_list.append({
                "size": n,
                "seed": seed,
                "solved": solved,
                "steps": steps,
                "time_seconds": run_time,
                "max_steps": max_steps,
            })

        success_rate = (solved_count / runs_per_size) * 100 if runs_per_size > 0 else 0
        avg_steps = total_steps / solved_count if solved_count > 0 else float("nan")
        avg_time = total_time / runs_per_size if runs_per_size > 0 else float("nan")

        logger.info(
            f"  Size {n}: Success Rate={success_rate:.2f}%, Avg Steps (solved)={avg_steps:.2f}, Avg Time={avg_time:.4f}s"
        )

    if results_list:
        results_df = pd.DataFrame(results_list)
        results_df.to_csv(results_file, index=False)
        logger.info(f"Analysis complete. Results saved to {results_file}")
        return results_file
    else:
        logger.warning("No results generated.")
        return None


def plot_analysis_results(csv_file_path: Path, runs_per_size: int):
    """Generate and save plots from the analysis results CSV file using OOP interface."""
    logger.info(f"Loading results from {csv_file_path} for plotting...")
    try:
        df = pd.read_csv(csv_file_path)
    except Exception as e:
        logger.exception(f"Error loading CSV file {csv_file_path}: {e}")  # noqa: TRY401
        return

    output_dir = csv_file_path.parent

    # Calculate statistics per size
    grouped = df.groupby("size")
    stats = grouped.agg(
        avg_time=("time_seconds", "mean"),
        std_time=("time_seconds", "std"),
        success_rate=("solved", lambda x: x.mean() * 100),
    )

    # Calculate step statistics only for solved instances
    solved_df = df[df["solved"]]
    solved_grouped = solved_df.groupby("size")
    step_stats = solved_grouped.agg(avg_steps=("steps", "mean"), std_steps=("steps", "std"))

    # Merge stats
    stats = stats.join(step_stats, how="left")
    stats = stats.fillna(0)  # Fill NaN std devs or steps

    # Plotting
    plt.style.use("seaborn-v0_8-paper")

    plot_title_suffix = f" ({runs_per_size} runs per size)"
    fig_size = (6, 4)
    common_opts = {"fmt": "-o", "markersize": 4, "capsize": 3}
    grid_opts = {"linestyle": "--", "alpha": 0.6}

    # 1. Average Time vs Size
    fig, ax = plt.subplots(figsize=fig_size)
    ax.errorbar(
        stats.index,
        stats["avg_time"],
        yerr=stats["std_time"],
        label="Avg Time",
        **common_opts,
    )
    ax.set_xlabel("Board Size (N)")
    ax.set_ylabel("Average Time (seconds)")
    ax.set_title("N-Queens: Average Time vs Board Size" + plot_title_suffix)
    ax.legend()
    ax.grid(True, **grid_opts)
    time_plot_path = output_dir / "n_queens_avg_time.svg"
    fig.savefig(time_plot_path, bbox_inches="tight")
    logger.info(f"Saved time plot to {time_plot_path}")
    plt.close(fig)

    # 2. Average Steps (Solved) vs Size
    fig, ax = plt.subplots(figsize=fig_size)
    ax.errorbar(
        stats.index,
        stats["avg_steps"],
        yerr=stats["std_steps"],
        label="Avg Steps (Solved)",
        **common_opts,
    )
    ax.set_xlabel("Board Size (N)")
    ax.set_ylabel("Average Steps (solved instances)")
    ax.set_title("N-Queens: Average Steps vs Board Size" + plot_title_suffix)
    ax.legend()
    ax.grid(True, **grid_opts)
    steps_plot_path = output_dir / "n_queens_avg_steps.svg"
    fig.savefig(steps_plot_path, bbox_inches="tight")
    logger.info(f"Saved steps plot to {steps_plot_path}")
    plt.close(fig)

    # 3. Success Rate vs Size
    fig, ax = plt.subplots(figsize=fig_size)
    ax.plot(stats.index, stats["success_rate"], "-o", markersize=4, label="Success Rate")
    ax.set_xlabel("Board Size (N)")
    ax.set_ylabel("Success Rate (%)")
    ax.set_title("N-Queens: Success Rate vs Board Size" + plot_title_suffix)
    ax.set_ylim(-5, 105)
    ax.legend()
    ax.grid(True, **grid_opts)
    success_plot_path = output_dir / "n_queens_success_rate.svg"
    fig.savefig(success_plot_path, bbox_inches="tight")
    logger.info(f"Saved success rate plot to {success_plot_path}")
    plt.close(fig)


if __name__ == "__main__":
    output_directory = Path(__file__).parent.parent.parent.parent / "results" / "n_queens"
    num_iterations_to_run = 100
    runs_per_size_to_run = 25

    results_csv = run_analysis(
        output_directory,
        num_iterations=num_iterations_to_run,
        runs_per_size=runs_per_size_to_run,
    )

    if results_csv:
        plot_analysis_results(results_csv, runs_per_size=runs_per_size_to_run)
