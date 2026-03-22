import pandas as pd
import pytest
from src.ztest import run_ztest


def make_df(n_control, conv_control, n_treatment, conv_treatment):
    """Helper to create a minimal test dataframe."""
    control = pd.DataFrame({
        'con_treat': ['control'] * n_control,
        'converted': [1] * conv_control + [0] * (n_control - conv_control)
    })
    treatment = pd.DataFrame({
        'con_treat': ['treatment'] * n_treatment,
        'converted': [1] * conv_treatment + [0] * (n_treatment - conv_treatment)
    })
    return pd.concat([control, treatment], ignore_index=True)


def test_output_keys():
    """Result should contain all expected keys."""
    df = make_df(1000, 120, 1000, 130)
    result = run_ztest(df, 'con_treat', 'treatment', 'control', 'converted')
    expected_keys = {'p_control', 'p_treatment', 'observed_diff',
                     'z_score', 'p_value', 'ci_lower', 'ci_upper', 'conclusion'}
    assert set(result.keys()) == expected_keys


def test_rejects_h0_when_large_effect():
    """Should reject H0 when treatment conversion is clearly higher."""
    df = make_df(10000, 1000, 10000, 1500)
    result = run_ztest(df, 'con_treat', 'treatment', 'control', 'converted')
    assert result['conclusion'] == 'Reject H0'
    assert result['p_value'] < 0.05


def test_fails_to_reject_h0_when_no_effect():
    """Should fail to reject H0 when conversion rates are identical."""
    df = make_df(10000, 1200, 10000, 1200)
    result = run_ztest(df, 'con_treat', 'treatment', 'control', 'converted')
    assert result['conclusion'] == 'Fail to reject H0'
    assert result['p_value'] >= 0.05


def test_observed_diff_is_correct():
    """Observed difference should equal p_treatment - p_control."""
    df = make_df(1000, 100, 1000, 150)
    result = run_ztest(df, 'con_treat', 'treatment', 'control', 'converted')
    expected_diff = round(0.15 - 0.10, 4)
    assert result['observed_diff'] == expected_diff


def test_p_control_and_treatment_correct():
    """Conversion rates should be computed correctly."""
    df = make_df(1000, 200, 1000, 300)
    result = run_ztest(df, 'con_treat', 'treatment', 'control', 'converted')
    assert result['p_control'] == 0.2
    assert result['p_treatment'] == 0.3
