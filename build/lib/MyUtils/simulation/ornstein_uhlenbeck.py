# =============================================================================
# PACKAGES
# =============================================================================
import numpy as np
import numpy.linalg as la
import scipy.linalg as sla
# =============================================================================
# FUNCTIONS
# =============================================================================
# UNIVARIATE


def univariate(x_0, kappa, theta, sigma, times, no_sims):
    """
    Ornstein-Uhlenbeck simulations
    """
    bm = np.random.normal(size=(times, no_sims))
    ou = np.zeros_like(bm)
    ou[0] = x_0

    for i in range(1, times):
        ou[i] = (np.exp(-kappa) * ou[i - 1]
                 + theta * (1 - np.exp(-kappa))
                 + sigma * np.sqrt(1 / (2 * kappa)
                                   * (1 - np.exp(-2 * kappa))) * bm[i])
    return ou


def univariate_Euler(x_0, kappa, theta, sigma, times, ts=1):
    """
    Ornstein-Uhlenbeck simulations based on Euler approximation
    """
    ou = [x_0]
    bm = np.random.normal(size=times)
    for i in range(1, times):
        drift = kappa * (theta - ou[i - 1]) * ts
        diffusion = sigma * np.sqrt(ts) * bm[i]
        ou.append(ou[i - 1] + drift + diffusion)
    return ou

# MULTIVARIATE


def alphav(x):
    """
    compute [exp(x) - 1]/x

    when x is a vector, (alpha(x) => see Koijen et al. (2005))
    """
    nc = x.shape[0]
    ax = np.expm1(x)
    for c in range(0, nc):
        if x[c] != 0.0:
            ax[c] /= x[c]
        else:
            ax[c] = 1.0
    return ax


def alpham(x):
    """
    compute [exp(x) - 1]/x

    when x is a matrix, (alpha(x) => see Koijen et al. (2005))
    """
    nr, nc = x.shape
    ax = np.expm1(x)
    for r in range(0, nr):
        for c in range(0, nc):
            if x[r, c] != 0.0:
                ax[r, c] /= x[r, c]
            else:
                ax[r, c] = 1.0
    return ax


def multivariate_parameters(Theta, Kappa, Sigma):
    """
    Returns the elements for of an multivariate OU, based on ou  parameters
    dY_t = (Theta_0 + Theta_1 @ Y_t)dt + Sigma_Y @ dZ_t
    """
    Theta0 = Theta
    Theta1 = -Kappa
    Sigma_Y = Sigma

    return Theta0, Theta1, Sigma_Y


def mu_Gamma_Sigma_h(Theta_0, Theta_1, Sigma_Y, h):
    """
    Computes the elements for an exact discretization of the multivariate OU
    process.
    Y_{t+h} = mu_h + Gamma_h @ Y_t + eps_{t+h} with eps_{t+h} ~ N(0, Sigma_h)
    """

    l, v = la.eig(Theta_1)
    no_factors = len(Theta_0)

    # mu
    F = h * np.diag(alphav(l * h))
    mu = v @ F @ la.inv(v) @ Theta_0

    # Gamma
    G = sla.expm(Theta_1 * h)

    # Sigma
    sqrtV = la.inv(v) @ Sigma_Y
    lam = np.kron(np.ones((no_factors, 1)), l)
    A = (lam + lam.T) * h
    V = sqrtV @ sqrtV.T * h * alpham(A)
    Sigma_h = v @ V @ v.T

    return mu, G, Sigma_h


def multivariate(Y_0, Theta_0, Theta_1, Sigma_Y, no_times, h, no_sims):
    """
    Simulates a multivariate OU process
    OU: dX_t = K(Theta - X_t)dt + Sigma * dW_t
    OU: DY_t = (Theta0 + Theta1 * Y_t)dt + Sigma_Y * dZ_t
    simulations: Y_tilde_{t+h} = mu_h + Gamma_h * Y_tilde_t + eps_{t+h}
    with eps_{t+h} ~ N(0, Sigma_h)    
    """
    no_factors = len(Y_0)

    # transform OU parameters into mu_h, Gamma_h, Sigma_h for simulations
    mu_h, Gamma_h, Sigma_h = mu_Gamma_Sigma_h(Theta_0, Theta_1, Sigma_Y, h)

    S = la.cholesky(Sigma_h)  # S @ S = Sigma_h

    eps = np.random.normal(0., 1., (no_sims, no_factors, no_times))

    eps = S @ eps

    Y_t = np.zeros_like(eps)

    # Evolve the state-variables for all remaining times
    # first observation
    Y_t[:, :, 0] = mu_h + Gamma_h @ Y_0 + eps[:, :, 0]

    # future observations
    for t in range(0, no_times - 1):
        Y_t[:, :, t + 1] += (mu_h + Y_t[:, :, t] @ Gamma_h.transpose()
                             + eps[:, :, t + 1])
    return Y_t
