import numpy as np
from scipy import stats


def run_ztest(df, group_col, treatment_val, control_val, outcome_col, alpha=0.05):
    """
    Run a one-tailed z-test for proportions.

    Parameters
    ----------
    df: pd.DataFrame
    group_col: str - column identifying control/treatment 
    treatment_val: str - value representing treatment group
    control_val: str - value representing control group
    outcome_col: str - binary outcome column (0/1)
    alpha: float - significance level, default 0.05

    Returns
    -------

    dict with z_score, p_value, ci_lower, ci_upper, conclusion
    """


    control = df[df[group_col] == control_val][outcome_col]
    treatment = df[df[group_col] == treatment_val][outcome_col]

    n_control = len(control)
    n_treatment = len(treatment)

    conv_control = control.sum()
    conv_treatment = treatment.sum()

    p_control = conv_control / n_control
    p_treatment = conv_treatment / n_treatment

    p_pool = (conv_control + conv_treatment) / (n_control + n_treatment)
    se = np.sqrt(p_pool * (1 - p_pool) * (1 / n_control + 1 / n_treatment))

    z_score = (p_treatment - p_control) / se
    p_value = stats.norm.cdf(z_score)

    z_crit = stats.norm.ppf(1 - alpha)
    ci_lower = (p_treatment - p_control) - z_crit * se 
    ci_upper = (p_treatment - p_control) + z_crit * se

    conclusion = "Reject H0" if p_value < alpha else "Fail to reject H0"

    return {
        "p_control": round(float(p_control), 4),
        "p_treatment": round(float(p_treatment), 4),
        "observed_diff": round(float(p_treatment - p_control), 4),
        "z_score": round(float(z_score), 4),
        "p_value": round(float(p_value), 4),
        "ci_lower": round(float(ci_lower), 4),
        "ci_upper": round(float(ci_upper), 4),
        "conclusion": conclusion
    }