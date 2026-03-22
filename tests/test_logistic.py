import pandas as pd
import pytest
from src.logistic import run_logistic_regression


def make_df(n_control, conv_control, n_treatment, conv_treatment):
    """Helper to create a minimal test dataframe."""
    control = pd.DataFrame({
        'is_treatment': [0] * n_control,
        'converted': [1] * conv_control + [0] * (n_control - conv_control)
    })
    treatment = pd.DataFrame({
        'is_treatment': [1] * n_treatment,
        'converted': [1] * conv_treatment + [0] * (n_treatment - conv_treatment)
    })
    return pd.concat([control, treatment], ignore_index=True)


def test_output_keys():
    """Result should contain all expected keys."""
    df = make_df(1000, 120, 1000, 130)
    result = run_logistic_regression(df, 'is_treatment', 'converted')
    expected_keys = {'coefficient', 'p_value', 'odds_ratio',
                     'ci_lower', 'ci_upper', 'conclusion'}
    assert set(result.keys()) == expected_keys


def test_positive_coefficient_when_treatment_converts_better():
    """Coefficient should be positive when treatment outperforms control."""
    df = make_df(10000, 1000, 10000, 2000)
    result = run_logistic_regression(df, 'is_treatment', 'converted')
    assert result['coefficient'] > 0


def test_odds_ratio_above_one_when_treatment_better():
    """Odds ratio should be above 1 when treatment converts better."""
    df = make_df(10000, 1000, 10000, 2000)
    result = run_logistic_regression(df, 'is_treatment', 'converted')
    assert result['odds_ratio'] > 1


def test_rejects_h0_when_large_effect():
    """Should reject H0 when treatment effect is large."""
    df = make_df(10000, 1000, 10000, 2000)
    result = run_logistic_regression(df, 'is_treatment', 'converted')
    assert result['conclusion'] == 'Reject H0'
    assert result['p_value'] < 0.05


def test_fails_to_reject_h0_when_no_effect():
    """Should fail to reject H0 when conversion rates are identical."""
    df = make_df(10000, 1200, 10000, 1200)
    result = run_logistic_regression(df, 'is_treatment', 'converted')
    assert result['conclusion'] == 'Fail to reject H0'
    assert result['p_value'] >= 0.05