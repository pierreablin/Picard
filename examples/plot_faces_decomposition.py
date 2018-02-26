"""
=======================================================
Blind source separation using preconditioned ICA on EEG
=======================================================

This example compares FastICA and Picard-O:

Pierre Ablin, Jean-François Cardoso, Alexandre Gramfort
"Faster ICA under orthogonal constraint"
ArXiv Preprint, Nov 2017
https://arxiv.org/abs/1711.10873

"""  # noqa

# Author: Pierre Ablin <pierre.ablin@inria.fr>
#         Alexandre Gramfort <alexandre.gramfort@inria.fr>
# License: BSD 3 clause


import numpy as np
from time import time
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_olivetti_faces
from sklearn.decomposition import fastica

from picard import picard


print(__doc__)

n_row, n_col = 2, 3
n_components = n_row * n_col
image_shape = (64, 64)
rng = np.random.RandomState(0)

###############################################################################
# Load faces data
dataset = fetch_olivetti_faces(shuffle=True, random_state=rng)
faces = dataset.data

n_samples, n_features = faces.shape

# global centering
faces_centered = faces - faces.mean(axis=0)

# local centering
faces_centered -= faces_centered.mean(axis=1).reshape(n_samples, -1)

print("Dataset consists of %d faces" % n_samples)


def gradient_norm(Y):
    psiY = np.tanh(Y)
    psidY_mean = 1 - np.mean(psiY ** 2, axis=1)
    g = np.dot(psiY, Y.T) / Y.shape[1]
    signs = np.sign(psidY_mean - np.diag(g))
    g *= signs[:, None]
    g = (g - g.T) / 2
    return np.linalg.norm(g)


def plot_gallery(title, images, n_col=n_col, n_row=n_row):
    plt.figure(figsize=(2. * n_col, 2.26 * n_row))
    plt.suptitle(title, size=16)
    for i, comp in enumerate(images):
        plt.subplot(n_row, n_col, i + 1)
        vmax = max(comp.max(), -comp.min())
        plt.imshow(comp.reshape(image_shape), cmap=plt.cm.gray,
                   interpolation='nearest',
                   vmin=-vmax, vmax=vmax)
        plt.xticks(())
        plt.yticks(())
    plt.subplots_adjust(0.01, 0.05, 0.99, 0.93, 0.04, 0.)

###############################################################################
# Run Picard-O and FastICA, and show the results


algorithms = [('Picard-O', picard),
              ('FastICA', fastica)]
for name, algorithm in algorithms:
    print("Running %s" % name)
    if name == 'FastICA':
        X = faces_centered.T
    else:
        X = faces_centered
    t0 = time()
    K, W, Y = algorithm(X, n_components=n_components)
    train_time = time() - t0
    if name == 'FastICA':
        Y = Y.T * np.sqrt(n_samples)  # Normalize so that Cov = Id
    Y *= np.sign(np.mean(Y ** 3, axis=1))[:, None]  # Fix the signs
    plot_gallery('%s - Time %.2fs - Gradient norm %.2e' %
                 (name, train_time, gradient_norm(Y)),
                 Y[:n_components])
plt.show()