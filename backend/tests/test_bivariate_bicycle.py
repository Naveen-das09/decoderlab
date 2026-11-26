from hashlib import sha256

import numpy as np

from decoderlab.bivariate_bicycle import bb72_parity_checks


def gf2_rank(matrix):
    """Count pivots using binary row elimination."""
    rows = matrix.copy()
    rank = 0
    for column in range(rows.shape[1]):
        pivots = np.flatnonzero(rows[rank:, column])
        if not pivots.size:
            continue
        pivot = rank + pivots[0]
        rows[[rank, pivot]] = rows[[pivot, rank]]
        below = rank + 1 + np.flatnonzero(rows[rank + 1:, column])
        rows[below] ^= rows[rank]
        rank += 1
    return rank


def test_published_bb72_check_matrices():
    hx, hz = bb72_parity_checks()
    for matrix in (hx, hz):
        assert matrix.shape == (36, 72)
        assert matrix.dtype == np.uint8
        assert np.all((matrix == 0) | (matrix == 1))
        assert np.all(matrix.sum(axis=1) == 6)
        assert np.all(matrix.sum(axis=0) == 3)
        assert gf2_rank(matrix) == 30

    assert not np.any((hx @ hz.T) % 2)
    assert hx.shape[1] - gf2_rank(hx) - gf2_rank(hz) == 12
    assert sha256(hx.tobytes(order="C")).hexdigest() == (
        "5ba3e05b4407c4584fd585cd52b714a1a432dc08ec7d1a3d243ffb66b8458838"
    )
    assert sha256(hz.tobytes(order="C")).hexdigest() == (
        "ffc3405373dc5afa63f51be84d8c7f1d31a973e4334a8d60dd70fb2e5368d63b"
    )


def test_bb72_perfect_z_syndrome_references_for_x_errors():
    hx, hz = bb72_parity_checks()
    error = np.zeros(72, dtype=np.uint8)
    assert not np.any((hz @ error) % 2)

    # Single X errors on the first qubit of each block.
    for qubit, expected_checks in ((0, [3, 24, 30]), (36, [4, 5, 18])):
        error[qubit] = 1
        np.testing.assert_array_equal(np.flatnonzero((hz @ error) % 2), expected_checks)
        error[qubit] = 0

    # A syndrome-free X operator outside the X-stabilizer row span.
    error[[0, 3, 6, 15, 24, 30]] = 1
    assert not np.any((hz @ error) % 2)
    assert gf2_rank(np.vstack((hx, error))) == 31
