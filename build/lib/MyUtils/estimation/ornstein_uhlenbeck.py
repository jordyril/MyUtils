# =============================================================================
# Packages
# =============================================================================
import numpy as np
import pandas as pd

# =============================================================================
# UNIVARIATE
# =============================================================================


def closed_form_observational_ll_univariate(x, x0, de, param):
    """
    Function computes the logdensity for the Vasicek model.
    Function is written in this form, with the purpose that 
    it can be used in the already written structure of Ait-Sahalia
    """
    kappa = param[0]
    theta = param[1]
    sigma = param[2]

    output = ((2 * np.pi)**(-1 / 2)
              * (sigma**2 / (2 * kappa) * (1 - np.exp(-2 * kappa * de)))**(-1 / 2)
              * np.exp(-(x - theta - (x0 - theta) * np.exp(-kappa * de))**2
                       / (2 * sigma**2 / (2 * kappa) * (1 - np.exp(-2 * kappa * de)))))

    return np.log(output)


def loglikelihood_vasicek(param, data):
    """
    Given a dataset, this function computes the loglikelihood of the parameters
    on this dataset
    """
    data = data.reshape(-1)

    x_0 = data[:-1]
    x = data[1:]

    return closed_form_observational_ll_univariate(x, x_0, 1, param).sum()


def ou_param_from_lr_param(lr_param):
    """
    Given the results from a Gaussian AR(1) parameter estimation (linear
    regression), this function transforms these results into the OU parameters
    """
    a, b, sigma_e = lr_param

    theta = a / (1 - b)
    kappa = - np.log(b)
    sigma = sigma_e * np.sqrt(-2 * np.log(b) / (1 - b**2))

    param = np.array([kappa, theta, sigma])

    return param


def lr_param_from_ou_param(param):
    """
    Given the parameters from an OU process, this function transforms these 	results into the parameters for a Gaussian AR(1) process
    """
    kappa, theta, sigma = param

    b = np.exp(-kappa)
    a = theta * (1 - b)

    sigma_e = sigma * np.sqrt((1 - b**2) / (2 * kappa))

    lr_param = np.array([a, b, sigma_e])

    return lr_param


def AR_p_ll(param, data):
    """
    Computes the loglikelihood of a Gaussian Autoregressive(p) process (AR(p))
    """
    p = len(param) - 2
    y_t = data[p:]
    y_tmps = np.zeros((p, len(y_t)))
    for i in range(p):
        y_tmps[i] = data[p - i - 1: -i - 1]

    # parameters
    a = param[0]
    b = param[1:p + 1]
    sigma_e = param[-1]
    T = len(y_t)

    y_t_hat = a + b @ y_tmps  # estimates

    errors = y_t - y_t_hat

    ll = (- T / 2 * np.log(2 * np.pi * sigma_e**2)
          - 1 / 2 * np.sum(errors**2 / sigma_e**2))

    return ll


def ou_univariate_parameter_estimation_ML(x, delta=1):
    """
    Analytical solution of the MLE estimation using the conditional probability
    density function
    """
    x = np.array([])
    y = np.array([])
    for i in t.T:
        x = np.hstack((x, i[:-1]))
        y = np.hstack((y, i[1:]))

    S_x = x.sum()
    S_y = y.sum()
    S_xx = (x**2).sum()
    S_xy = (x * y).sum()
    S_yy = (y**2).sum()

    n = t.shape[0] * t.shape[1] - t.shape[1]

    theta = (S_y * S_xx - S_x * S_xy) / \
        (n * (S_xx - S_xy) - (S_x**2 - S_x * S_y))
    kappa = -1 / delta * np.log((S_xy - theta * S_x - theta * S_y + n * theta**2) /
                                (S_xx - 2 * theta * S_x + n * theta**2))

    alpha = np.exp(-kappa * delta)

    sigma_hat_squared = 1 / n * (S_yy - 2 * alpha * S_xy + alpha**2 * S_xx -
                                 2 * theta * (1 - alpha) * (S_y - alpha * S_x) +
                                 n * theta**2 * (1 - alpha)**2)

    sigma = np.sqrt(sigma_hat_squared * 2 * kappa / (1 - alpha**2))

    return kappa, theta, sigma


def mle_var_kappa(kappa_hat, de=1):
    """
    Maximum likelihood variance of kappa
    """
    var = np.exp(2 * de * kappa_hat) / de**2
    return var


def mle_var_theta(kappa_hat, sigma_hat, de=1):
    """
    Maximum likelihood variance of Theta
    """
    var = ((sigma_hat**2 * (np.exp(de * kappa_hat) + 1)) /
           (2 * (np.exp(de * kappa_hat) - 1) * kappa_hat))
    return var


def mle_var_sigma(kappa_hat, sigma_hat, de=1):
    """
    Maximum likelihood variance of sigma
    """
    var = (sigma_hat**2 / 4 *
           (((np.exp(2 * de * kappa_hat) - 1)**2
             + 2 * de**2 * kappa_hat**2 * (np.exp(2 * de * kappa_hat) + 1)
             - 4 * de * kappa_hat * (np.exp(2 * de * kappa_hat) - 1)) /
            (de**2 * (np.exp(2 * de * kappa_hat) - 1) * kappa_hat**2))
           )
    return var
# =============================================================================
# MULTIVARIATE
# =============================================================================
# VAR(p)


def loglikelihood_gaussian_VARp(param, t):
    """
    Computes the loglikelihood function of a k-factor Var(p) process given 
    the parameters and the data.
    Based on 3.4.5 in Lutkepohl(2007)
    parameters consists of an array with the first k elements being the 
    estimates for mu (k process averages), remaining elements of the 
    parameters array are the estimates for kxpk A matrix.
    """
    k = t.shape[0]
    p = int((len(param) - k) / k**2)
    T = t.shape[1] - p  # first p observations are assumed known

    mu = devec(param[:k], (k, 1))

    A_is = param[k:]  # elements for A matrix

    A = devec(A_is, (k, k * p))

    Y = t[:, p:]  # all 'unknown' observations

    Y0 = np.subtract(Y, mu)

    X = np.subtract(t[:, :-p], mu)

    U = Y0 - A @ X

    sigma_U = U @ U.T / T

    # Note the pseudo inverse - after weeks of struggle, I found out that the
    # normal inv and numba does not do well for 'big' numbers, giving
    # completely wrong results after annealing. This is (hopefully) solved
    # by using the pseudo-inv
    ll = (- 1 / 2 * k * T * np.log(2 * np.pi)
          - T / 2 * np.log(la.det(sigma_U))
          - trace(U.T @ la.pinv(sigma_U) @ U))

    return ll, sigma_U

### Var(1) - restricted


def param_to_mu_A1_restricted(parameters):
    """
    Tranforms parameter array for an 2 factor Var(1) process, with the 
    restriction of the upper right corner being set to 0.
    """
    k = 2
    mu = np.zeros((k, 1))
    mu[0] = parameters[0]
    mu[1] = parameters[1]

    A1 = np.zeros((k, k))
    A1[0][0] = parameters[2]
    A1[1][0] = parameters[3]
    A1[1][1] = parameters[4]
    return mu, A1


def loglikelihood_gaussian_twofactorVAR1_restricted(parameters, data):
    """
    Computes the loglikelihood function of a 2-factor Var(1) process given 
    the parameters and the data.
    Based on 3.4.5 in Lutkepohl(2007)
    parameters consists of an array with the first two elements being the 
    estimates for mu (2 process averages), remaining 3 elements of the 
    parameters array are the estimates for the lower triangle of the kxk A1
    matrix. Upper part is constrained to 0.
    """
    k = 2
    p = 1
    T = data.shape[1] - p

    mu, A1 = param_to_mu_A1_restricted(parameters)

    Y = data[:, p:]

    Y0 = np.subtract(Y, mu)

    X = np.subtract(data[:, :-p], mu)

    U = Y0 - A1 @ X
    Sigma_u = U @ U.T / T

    ll = (-k * T * 1 / 2 * np.log(2 * np.pi)
          - T / 2 * np.log(la.det(Sigma_u))
          - 1 / 2 * trace(U.T @ la.pinv(Sigma_u) @ U))

    return ll, Sigma_u
