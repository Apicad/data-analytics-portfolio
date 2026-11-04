#!/usr/bin/env python
"""Command-line salary predictor.

PORTFOLIO IMPROVEMENT. The original capstone ended with an interactive input()
prompt that asked for a name and years of experience. This is the same idea as a
proper command-line tool, plus a 95% prediction interval and a warning when the
experience you ask about is outside the range the data covers.

Usage:
    python predict.py --years 5
    python predict.py --years 5 --name Abdiel
"""
import argparse

import salary_model as model


def main() -> None:
    parser = argparse.ArgumentParser(description="Predict salary from years of experience.")
    parser.add_argument("--years", type=float, required=True, help="years of experience, e.g. 5 or 2.5")
    parser.add_argument("--name", default=None, help="optional name to address the answer to")
    args = parser.parse_args()

    df = model.load_data()
    result = model.fit_ols(df)
    row = model.prediction_intervals(result, args.years).iloc[0]

    who = f"{args.name}, " if args.name else ""
    print(f"{who}for {args.years:g} years of experience the model predicts ${row.predicted:,.0f}.")
    print(f"95% prediction interval for one person: ${row.pi_low:,.0f} to ${row.pi_high:,.0f}.")

    low, high = df["YearsExperience"].min(), df["YearsExperience"].max()
    if not low <= args.years <= high:
        print(
            f"Heads up: the data only covers {low:g} to {high:g} years of experience. "
            "Outside that range this is a straight-line guess, not something the data supports."
        )


if __name__ == "__main__":
    main()
