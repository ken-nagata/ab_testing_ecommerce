import numpy as np
import statsmodels.api as sm 

def run_logistic_regression(df, treatment_col, outcome_col):
    """
    Run logistic regression to estiamte treatment effect on a binary outcome.

    Parameters
    ----------
    df : pd.DataFrame
    treatment_col : str - binary column (1 = treatment, 0 = control)
    outcome_col : str - binary outcome column (0/1)

    Returns 
    -------
    dict with coefficient, p_value, odds_ratio, ci_lower, ci_upper
    """

    X = sm.add_constant(df[treatment_col])
    y = df[outcome_col]

    model = sm.Logit(y, X)
    result = model.fit(disp=0)

    coef = result.params[treatment_col]
    p_value = result.pvalues[treatment_col]
    odds_ratio = np.exp(coef)
    ci = result.conf_int()
    ci_lower = np.exp(ci.loc[treatment_col, 0])
    ci_upper = np.exp(ci.loc[treatment_col, 1])

    return {
        "coefficient": round(float(coef), 4),
        "p_value": round(float(p_value), 4),
        "odds_ratio": round(float(odds_ratio), 4),
        "ci_lower": round(float(ci_lower), 4),
        "ci_upper": round(float(ci_upper), 4),
        "conclusion": "Reject H0" if p_value < 0.05 else "Fail to reject H0"
    }