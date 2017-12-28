# Authors: Pierre Ablin <pierre.ablin@inria.fr>
#          Alexandre Gramfort <alexandre.gramfort@inria.fr>
#          Jean-Francois Cardoso <cardoso@iap.fr>
#
# License: BSD (3-clause)

import numpy as np

from scipy.linalg import expm

import numexpr as ne


def score(Y):
    return ne.evaluate('tanh(Y)')


def score_der(psiY):
    return -np.mean(psiY ** 2, axis=1) + 1.


def gradient(Y, psiY):
    '''
    Compute the gradient for the current signals
    '''
    _, T = Y.shape
    return np.inner(psiY, Y) / float(T)


def proj_hessian_approx(Y, psidY_mean, G):
    '''
    Computes the projected Hessian approximation.
    '''
    N, _ = Y.shape
    diag = psidY_mean[:, None] * np.ones(N)[None, :]
    off_diag = np.diag(G)
    return 0.5 * (diag + diag.T - off_diag[:, None] - off_diag[None, :])


def regularize_hessian(h, l):
    '''
    Clips the eigenvalues of h to l
    '''
    h[h < l] = l
    return h


def solve_hessian(G, h):
    '''
    Returns the inverse Hessian times G
    '''
    return G / h


def loss(Y, signs):
    '''
    Returns the loss function
    '''
    output = 0.
    _, T = Y.shape
    for y, s in zip(Y, signs):
        output += s * ne.evaluate('sum(abs(y) + log1p(exp(-2. * abs(y))))') / T
    return output


def l_bfgs_direction(G, h, s_list, y_list, r_list):
    q = G.copy()
    a_list = []
    for s, y, r in zip(reversed(s_list), reversed(y_list), reversed(r_list)):
        alpha = r * np.sum(s * q)
        a_list.append(alpha)
        q -= alpha * y
    z = solve_hessian(q, h)
    for s, y, r, alpha in zip(s_list, y_list, r_list, reversed(a_list)):
        beta = r * np.sum(y * z)
        z += (alpha - beta) * s
    return -z


def line_search(Y, signs, direction, current_loss, ls_tries):
    '''
    Performs a backtracking line search, starting from Y and W, in the
    direction direction.
    '''
    alpha = 1.
    if current_loss is None:
        current_loss = loss(Y, signs)
    for _ in range(ls_tries):
        Y_new = np.dot(expm(alpha * direction), Y)
        new_loss = loss(Y_new, signs)
        if new_loss < current_loss:
            return True, Y_new, new_loss, alpha
        alpha /= 2.
    else:
        return False, Y_new, new_loss, alpha
