"""Parity checks for the published [[72,12,6]] bivariate bicycle code."""

import numpy as np
from numpy.typing import NDArray


def bb72_parity_checks() -> tuple[NDArray[np.uint8], NDArray[np.uint8]]:
    """Return H_X = [A | B] and H_Z = [B.T | A.T] over GF(2).

    Columns in each 36-qubit block are ordered by the monomial x^i y^j,
    with index 6*i + j. A shift acts on a column vector by moving its
    nonzero entry to the row for the translated monomial.
    """
    order = 6
    columns = np.arange(order * order)
    x, y = np.divmod(columns, order)

    def polynomial(terms: tuple[tuple[int, int], ...]) -> NDArray[np.uint8]:
        matrix = np.zeros((columns.size, columns.size), dtype=np.uint8)
        for dx, dy in terms:
            rows = ((x + dx) % order) * order + (y + dy) % order
            matrix[rows, columns] ^= 1
        return matrix

    # Bravyi et al., arXiv:2308.07915v2, Table 3.
    a = polynomial(((3, 0), (0, 1), (0, 2)))
    b = polynomial(((0, 3), (1, 0), (2, 0)))
    return np.hstack((a, b)), np.hstack((b.T, a.T))
