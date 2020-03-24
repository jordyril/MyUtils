# =============================================================================
# Packages
# =============================================================================
import numpy as np
# =============================================================================
# support functions
# =============================================================================


def vec(x):
    """
    performs column stacking operator
    """
#    return x.reshape((-1, 1), order='F')
    return x.flatten(order='F')


def elimination_matrix_save_first_p_elements(p, k):
    """
    Return an elimination matrix of size pxk, with the first p elements of
    the diagonal being ones
    """
    p, k = int(p), int(k)
    L = np.zeros((p, k))
    for i in range(p):
        L[i, i] = 1
    return L


def devec(elements, shape=None):
    """
    Reverses the vec operation. In case no shape is given, a square matrix gets
    returned based on the lenght of th elements-array
    """
    if shape is not None:
        A = np.zeros(shape)
    else:
        k = int(np.sqrt(len(elements)))
        A = np.zeros((k, k))

    nbr_row = A.shape[0]
    nbr_col = A.shape[1]

    e = 0
    for i in range(nbr_col):
        for j in range(nbr_row):
            A[j][i] = elements[e]
            e += 1

    return A


def elimination_matrix_vech(k):
    """
    Constructs the elimination matrix that, multiplied with the vectorization
    of matrix x, returns the half-vectorization of matrix x
    """
    n = triangular_sum(k)
    L = np.zeros((n, k**2))
    row = 0
    column = 0
    for i in range(k, 0, -1):
        for _ in range(i):
            L[row][column] = 1
            row += 1
            column += 1
        column += k - i + 1

    return L


def duplication_matrix(m):
    """
    Given the shape m of a symmetric square matrix x, this function returns
    the duplication matrix D, such that D @ vech(x) = vec(x)
    """
    D = np.zeros((m**2, int(1 / 2 * m * (m + 1))))
    row = 0
    column = 0
    for i in range(m, 0, -1):
        for _ in range(i):
            D[row][column] = 1
            column += 1
            row += 1

        row += m - i + 1

    row = m
    column = 1
    for i in range(m - 1, 0, -1):
        for _ in range(i):
            D[row][column] = 1
            column += 1
            row += m
        column += 1
        row = m + (m - i) * (m + 1)

    return D


def vech(x):
    """
    performs column stacking operator on a matrix for only the elements on
    and below the diagonal
    """
    k = x.shape[0]
    L = elimination_matrix_vech(k)
    return L @ vec(x)


def devech(elements):
    """
    Reverses the vech operation.
    """
    e = 0
    k = reverse_triangular_sum(len(elements))
    A = np.zeros((k, k))

    # filing bottom triangle + diagonal
    row = 0
    col = 0
    for i in range(k):
        for j in range(k - 1, i - 1, -1):
            A[row][col] = elements[e]

            row += 1
            e += 1
        col += 1
        row = col

    # filling upper half (symmetric matrix)
    row = 0
    for i in range(k - 1):
        for j in range(k - 1, i, -1):
            A[row][j] = A[j][row]
        row += 1

    return A


def trace(x):
    n = x.shape[0]
    som = 0.
    for i in range(n):
        som += x[i, i]
    return som


def triangular_sum(n):
    """
    Computes the triangular sum of any positive natural number
    """
    if n == 1:
        return n

    elif n == 0:
        return 0

    else:
        return triangular_sum(n - 1) + n


def reverse_triangular_sum(x):
    """
    Returns the integer that leads to triangular number x
    """
    t = x
    i = 1
    while t > 0:
        t -= i
        i += 1
    try:
        assert t == 0, 'This is not a triangular number'
    except AssertionError:
        raise

    return i - 1


def sqrtMatrix(Sigma):
    """compute G such that GG' = Sigma """
    ev, U = np.linalg.eig(Sigma)
    G = U * np.sqrt(ev)

    return G
