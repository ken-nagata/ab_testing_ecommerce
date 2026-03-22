import pytest
from src.power import run_power_analysis


def test_output_keys():
    """Result should contain all expected keys."""
    result = run_power_analysis(p_baseline=0.12, mde=0.01, n_actual=10000)
    expected_keys = {'p_baseline', 'p_treatment_assumed', 'mde',
                     'effect_size_cohens_h', 'required_n_per_group',
                     'actual_n_per_group', 'actual_power'}
    assert set(result.keys()) == expected_keys


def test_required_n_decreases_with_larger_mde():
    """Larger MDE should require smaller sample size."""
    result_small_mde = run_power_analysis(p_baseline=0.12, mde=0.01, n_actual=10000)
    result_large_mde = run_power_analysis(p_baseline=0.12, mde=0.05, n_actual=10000)
    assert result_small_mde['required_n_per_group'] > result_large_mde['required_n_per_group']


def test_power_increases_with_larger_n():
    """Larger sample size should produce higher power."""
    result_small_n = run_power_analysis(p_baseline=0.12, mde=0.01, n_actual=1000)
    result_large_n = run_power_analysis(p_baseline=0.12, mde=0.01, n_actual=100000)
    assert result_small_n['actual_power'] < result_large_n['actual_power']


def test_actual_n_matches_input():
    """actual_n_per_group should match the n_actual input."""
    result = run_power_analysis(p_baseline=0.12, mde=0.01, n_actual=50000)
    assert result['actual_n_per_group'] == 50000


def test_p_treatment_assumed_correct():
    """p_treatment_assumed should equal p_baseline + mde."""
    result = run_power_analysis(p_baseline=0.12, mde=0.01, n_actual=10000)
    assert round(result['p_treatment_assumed'], 4) == round(0.12 + 0.01, 4)