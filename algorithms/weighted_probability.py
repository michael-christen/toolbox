"""Determine which bucket to fall in, given weighted probabilities.

For example, assume you have | A   | B   | C   |
                             | 10% | 30% | 60% |

how do you return A 10% of the time, B 30%, etc?
"""
import random


def get_weighted_random(probability_distribution):
    """Return an item in probability_distribution, such that we'd get a similar
    distribution over time.

    Args:
        - probability_distribution (list(float)): List of probabilities, which
        are [0, 1], and sum to 1.
    """
    assert abs(sum(probability_distribution) - 1.0) < 0.0001
    rchoice = random.random()
    for idx, probability in enumerate(probability_distribution):
        if rchoice < probability:
            return idx
        rchoice -= probability
    raise ValueError("Should never get here")
