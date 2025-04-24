# Demonstration Exercise 6/5

## Usage

```sh
$ uv run src/simulation/demo_6/e_approximation.py
{
  "estimate": 2.699,
  "variance": 0.74114,
  "95%_CI": [
    2.645642,
    2.752358
  ]
}
```

Running 100,000 simulations:
```sh
$ uv run src/simulation/demo_6/e_approximation.py --n-runs 100_000
{
  "estimate": 2.72006,
  "variance": 0.768241,
  "95%_CI": [
    2.714628,
    2.725492
  ]
}
```
