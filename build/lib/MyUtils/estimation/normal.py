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


def ci(mean, sigma_squared, n, alpha=0.05):
    """
    Computes confidence interval based on normal distribution
    """
    z_alpha = scs.norm.ppf(1 - alpha / 2)

    ci_bound = z_alpha * np.sqrt(sigma_squared / n)

    ci = np.array([mean - ci_bound, mean + ci_bound])

    ci = np.sort(ci)

    return ci


def loglikelihood_AR1(param, t):
    """
    Computes the loglikelihood for a Gaussian AR(1) process, given data and
    the suggested parameters
    """
    t = t.reshape(-1)
    y_1 = t[0]
    y_t = t[1:]
    y_tm1 = t[:-1]

    a, b, sigma_e = param
    T = len(t)

    ll_1 = (- 1 / 2 * np.log(2 * np.pi)
            - 1 / 2 * np.log(sigma_e**2 / (1 - b**2))
            - 1 / 2 * ((y_1 - a / (1 - b))**2 / (sigma_e**2 / (1 - b**2))))

    ll_1 = 0
    ll_t = (- (T - 1) / 2 * np.log(2 * np.pi * sigma_e**2)
            - 1 / 2 * np.sum((y_t - a - b * y_tm1)**2 / sigma_e**2))

    return ll_1 + ll_t
