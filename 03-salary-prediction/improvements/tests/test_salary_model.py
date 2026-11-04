"""Checks that the model reproduces the Year Up capstone numbers and behaves sensibly.

Run from the repo root or this project folder:  pytest
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import salary_model as model  # noqa: E402

# Figures quoted on the capstone slides (Drive deck "capstone - year up", CIS 304).
SLIDE_SLOPE = 9449.96
SLIDE_INTERCEPT = 25792.20
SLIDE_R2 = 0.957


@pytest.fixture(scope="module")
def data():
    return model.load_data()


@pytest.fixture(scope="module")
def result(data):
    return model.fit_ols(data)


def test_data_shape(data):
    assert list(data.columns) == ["YearsExperience", "Salary"]
    assert len(data) == 30


def test_coefficients_match_capstone_slides(result):
    s = model.summarize(result)
    assert s["slope"] == pytest.approx(SLIDE_SLOPE, abs=0.01)
    assert s["intercept"] == pytest.approx(SLIDE_INTERCEPT, abs=0.01)
    assert s["r_squared"] == pytest.approx(SLIDE_R2, abs=0.0005)


def test_slope_is_statistically_significant(result):
    assert model.summarize(result)["slope_p_value"] < 0.001


def test_predict_five_years(result):
    expected = SLIDE_INTERCEPT + 5 * SLIDE_SLOPE
    assert model.predict(result, 5)[0] == pytest.approx(expected, abs=0.5)


def test_predict_vectorised_and_increasing(result):
    preds = model.predict(result, [1, 2, 3, 10])
    assert preds.shape == (4,)
    assert np.all(np.diff(preds) > 0)


def test_predict_rejects_negative_years(result):
    with pytest.raises(ValueError):
        model.predict(result, -1)


def test_prediction_interval_wider_than_confidence_interval(result):
    row = model.prediction_intervals(result, 5).iloc[0]
    assert row["pi_low"] < row["ci_low"] < row["predicted"] < row["ci_high"] < row["pi_high"]


def test_load_data_rejects_wrong_columns(tmp_path):
    bad = tmp_path / "bad.csv"
    pd.DataFrame({"Years": [1, 2, 3], "Pay": [1, 2, 3]}).to_csv(bad, index=False)
    with pytest.raises(ValueError):
        model.load_data(bad)


def test_loocv_model_beats_mean_baseline(data):
    cv = model.leave_one_out_rmse(data)
    assert cv["n_folds"] == 30
    assert cv["model_rmse"] < cv["baseline_rmse"] / 2
