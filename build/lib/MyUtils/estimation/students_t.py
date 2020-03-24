"""
Created on Tue Jul 31 15:43:04 2018

@author: jordy
"""
# =============================================================================
# Packages
# =============================================================================
import numpy as np
import scipy.stats as scs

# =============================================================================
# FUNCTIONS
# =============================================================================


def ci(mean, sigma_squared, n, df, alpha=0.05):
    """
    Computes confidence interval based on students t distribution
    """
    t_alpha = scs.t.ppf(1 - alpha / 2, n - df)

    ci_bound = t_alpha * np.sqrt(sigma_squared)

    ci = np.array([mean - ci_bound, mean + ci_bound])

    ci = np.sort(ci)

    return ci
