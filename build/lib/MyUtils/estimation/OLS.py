# =============================================================================
# Packages
# =============================================================================
import statsmodels.api as sm
import numpy.linalg as la
# =============================================================================
# fFunctions
# =============================================================================


def regression(x, y, constant=True):
    """
    Perform ordinary OLS estimation

    :param x: exogenous variable vector/matrix
    :param y: endogenous variable vector
    :param constant: ols with or without constant

    Returns
    ----
    return : estimated parameters and the residuals

    """
    if constant:
        x = sm.add_constant(x)

    model = sm.OLS(y, x)
    results = model.fit()

    return results.params, results.resid


def var_estimate_small_sample(b_hat, eps):
    """
    Estimate \hat{sigma^2} from am OLS estimation
    """
    n = len(eps)
    K = len(b_hat)

    s2 = (eps @ eps) / (n - K)

    return s2


def var_estimators_small_sample(b_hat, x, eps):
    """
    Estimate the variance surrounding the OLS parameter estimations b_hat
    """
    s2 = var_estimate_small_sample(b_hat, eps)

    var_b_hat_hat = s2 * la.inv(x.T @ x)

    return var_b_hat_hat
