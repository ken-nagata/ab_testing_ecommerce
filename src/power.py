from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize

def run_power_analysis(p_baseline, mde, n_actual, alpha=0.05, power=0.80):
    """ 
    Run a power analysis for a two-proportion z-test.

    Parameters
    ----------
    p_baseline : float - baseline conversion rate (control group)
    mde : float - minimum detectable effect (e.g. 0.01 for 1pp lift)
    n_actual : int - actual sample size per group
    alpha: float - significance level, default 0.05
    power: float - desired power, default 0.80

    Returns
    -------
    dict with effect_size, required_n, actual_power
    """

    p_treatment_assumed = p_baseline + mde
    effect_size = proportion_effectsize(p_treatment_assumed, p_baseline)

    analysis = NormalIndPower()

    required_n = analysis.solve_power(
        effect_size =effect_size,
        alpha=alpha,
        power=power,
        alternative='larger'
    )

    actual_power = analysis.solve_power(
        effect_size=effect_size,
        alpha=alpha,
        nobs1=n_actual,
        alternative='larger'
    )


    return {
        "p_baseline": round(p_baseline, 4),
        "p_treatment_assumed": round(p_treatment_assumed, 4),
        "mde": round(mde, 4),
        "effect_size_cohens_h": round(float(effect_size), 4),
        "required_n_per_group": int(round(required_n)),
        "actual_n_per_group": n_actual,
        "actual_power": round(float(actual_power), 4)
    }