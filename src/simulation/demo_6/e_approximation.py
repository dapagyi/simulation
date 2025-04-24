import itertools
import json

import click
import numpy as np
from scipy.stats import norm


def simulate_once():
    uniforms = (np.random.uniform() for _ in itertools.count())
    cumulative = itertools.accumulate(uniforms)
    return next(i + 1 for i, total in enumerate(cumulative) if total > 1)


def estimate_e(n_runs=1000, confidence=0.95):
    samples = [simulate_once() for _ in range(n_runs)]
    mean = np.mean(samples)
    var = np.var(samples, ddof=1)
    se = np.sqrt(var / n_runs)
    z = norm.ppf(0.5 + confidence / 2)
    ci = (mean - z * se, mean + z * se)
    return {
        "estimate": round(mean, 6),
        "variance": round(var, 6),
        f"{int(confidence * 100)}%_CI": [round(ci[0], 6), round(ci[1], 6)],
    }


@click.command()
@click.option("--n-runs", default=1000, help="Number of simulation runs.")
@click.option("--confidence", default=0.95, help="Confidence level for interval.")
def main(n_runs, confidence):
    result = estimate_e(n_runs, confidence)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
