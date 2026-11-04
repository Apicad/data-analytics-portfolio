"""Salary vs. years of experience: a small, tested OLS model.

PORTFOLIO IMPROVEMENT (added 2026, not part of the original Year Up capstone).
The original capstone fit the same model inside one notebook. This module pulls
that logic into plain functions so the notebooks stay short and the headline
numbers (slope, intercept, R squared) can be checked automatically by pytest.

Data: ../original/Salary_Data.csv, the public Kaggle "Salary Data" set
(30 rows, columns YearsExperience and Salary).
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

HERE = Path(__file__).resolve().parent
DATA_PATH = HERE.parent / "original" / "Salary_Data.csv"
REQUIRED_COLUMNS = ("YearsExperience", "Salary")


def load_data(path: Path | str = DATA_PATH) -> pd.DataFrame:
    """Read the CSV and refuse to continue if it does not look like the capstone data."""
    df = pd.read_csv(path)
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"missing column(s) {missing}; expected {list(REQUIRED_COLUMNS)}")
    if df[list(REQUIRED_COLUMNS)].isna().any().any():
        raise ValueError("data has blank cells in YearsExperience or Salary")
    if len(df) < 3:
        raise ValueError("need at least 3 rows to fit a line")
    return df[list(REQUIRED_COLUMNS)].astype(float)


def fit_ols(df: pd.DataFrame):
    """Fit Salary = intercept + slope * YearsExperience with ordinary least squares."""
    x = sm.add_constant(df["YearsExperience"])
    return sm.OLS(df["Salary"], x).fit()


def _design(years) -> tuple[np.ndarray, np.ndarray]:
    years = np.atleast_1d(np.asarray(years, dtype=float))
    if np.isnan(years).any():
        raise ValueError("years of experience must be a number")
    if (years < 0).any():
        raise ValueError("years of experience cannot be negative")
    return years, sm.add_constant(years, has_constant="add")


def predict(result, years) -> np.ndarray:
    """Predicted salary for one or more years-of-experience values."""
    _, x = _design(years)
    return np.asarray(result.predict(x))


def prediction_intervals(result, years, alpha: float = 0.05) -> pd.DataFrame:
    """Point prediction plus two intervals.

    ci_*: where the *average* salary for that experience level probably sits.
    pi_*: where *one person's* salary probably sits. Always wider.
    """
    years, x = _design(years)
    frame = result.get_prediction(x).summary_frame(alpha=alpha)
    return pd.DataFrame(
        {
            "years": years,
            "predicted": frame["mean"].to_numpy(),
            "ci_low": frame["mean_ci_lower"].to_numpy(),
            "ci_high": frame["mean_ci_upper"].to_numpy(),
            "pi_low": frame["obs_ci_lower"].to_numpy(),
            "pi_high": frame["obs_ci_upper"].to_numpy(),
        }
    )


def summarize(result) -> dict:
    """The handful of numbers worth quoting."""
    return {
        "n": int(result.nobs),
        "intercept": float(result.params["const"]),
        "slope": float(result.params["YearsExperience"]),
        "slope_std_err": float(result.bse["YearsExperience"]),
        "slope_p_value": float(result.pvalues["YearsExperience"]),
        "r_squared": float(result.rsquared),
        "adj_r_squared": float(result.rsquared_adj),
        "residual_std": float(np.sqrt(result.scale)),
    }


def _rmse(errors) -> float:
    return float(np.sqrt(np.mean(np.square(errors))))


def leave_one_out_rmse(df: pd.DataFrame) -> dict:
    """Leave-one-out cross-validation.

    For each row: fit the line on the other 29 rows, predict this one, record the
    miss. Compared against a baseline that always guesses the mean salary.
    Answers "how far off is this line on someone it has never seen?"
    """
    years = df["YearsExperience"].to_numpy(dtype=float)
    salary = df["Salary"].to_numpy(dtype=float)
    model_errors, baseline_errors = [], []
    for i in range(len(df)):
        train = df.drop(df.index[i])
        res = fit_ols(train)
        model_errors.append(salary[i] - predict(res, years[i])[0])
        baseline_errors.append(salary[i] - train["Salary"].mean())
    return {
        "model_rmse": _rmse(model_errors),
        "baseline_rmse": _rmse(baseline_errors),
        "n_folds": len(df),
    }
