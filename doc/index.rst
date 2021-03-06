.. picard documentation master file, created by
   sphinx-quickstart on Mon May 23 16:22:52 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Picard
======

This is a library to run the Preconditioned ICA for Real Data (PICARD) algorithm [1]
and its orthogonal version (PICARD-O) [2]. These algorithms show fast convergence even
on real data for which sources independence do not perfectly hold.

Installation
------------

We recommend the `Anaconda Python distribution <https://www.continuum.io/downloads>`_.
Otherwise, to install ``picard``, you first need to install its dependencies::

	$ pip install numpy matplotlib numexpr scipy

Then install Picard::

	$ pip install python-picard

If you do not have admin privileges on the computer, use the ``--user`` flag
with `pip`. To upgrade, use the ``--upgrade`` flag provided by `pip`.

To check if everything worked fine, you can do::

	$ python -c 'import picard'

and it should not give any error message.

Quickstart
----------

The easiest way to get started is to copy the following lines of code
in your script:

.. code:: python

   >>> import numpy as np
   >>> from picard import picard
   >>> N, T = 3, 1000
   >>> S = np.random.laplace(size=(N, T))
   >>> A = np.random.randn(N, N)
   >>> X = np.dot(A, S)
   >>> K, W, Y = picard(X)  # doctest:+ELLIPSIS

Picard outputs the whitening matrix, `K`, the estimated unmixing matrix, `W`, and
the estimated sources `Y`. It means that:

.. math::

    Y = W K X

Bug reports
-----------

Use the `github issue tracker <https://github.com/pierreablin/picard/issues>`_ to report bugs.

Cite
----

   [1] Pierre Ablin, Jean-Francois Cardoso, and Alexandre Gramfort
   "Faster independent component analysis by preconditioning with Hessian approximations"
   IEEE Transactions on Signal Processing, 2018, https://arxiv.org/abs/1706.08171

   [2] Pierre Ablin, Jean-Francois Cardoso, and Alexandre Gramfort
   "Faster ICA under orthogonal constraint"
   ICASSP, 2018, https://arxiv.org/abs/1711.10873

API
---

.. toctree::
    :maxdepth: 1

    api.rst
