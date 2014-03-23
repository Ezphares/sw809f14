"""
An implementation of the Glicko system.

Calculates Glicko ratings and RDs for single-game rating periods.
The technical details of the Glicko system are described in:
http://www.glicko.net/glicko/glicko.pdf
"""

import math

class Glicko:

    """
    unranked_rd - The default RD assigned to unranked players (default 350).
    min_rd - The lowest possible RD of a player (default 30).
    c - Constant which governs the increase in uncertainty over time.
    """

    def __init__(self, c, unranked_rd=350, min_rd=30):
        self.unranked_rd = unranked_rd
        self.min_rd = min_rd
        self.c = c
        self.q = math.log(10) / 400

    def _g(self, rd):
        return 1 / math.sqrt(1 + 3 * self.q**2 * rd**2 / math.pi**2)

    def _E(self, rating, rating_opp, rd_opp):
        return 1 / (1 + 10**(-self._g(rd_opp) * (rating - rating_opp) / 400))

    def _d(self, rating, rating_opp, rd_opp):
        valE = self._E(rating, rating_opp, rd_opp)
        return 1 / (self.q**2 * self._g(rd_opp)**2 * valE * (1 - valE))

    def _update_rd(self, rd_old, t):
        return min(math.sqrt(rd_old**2 + self.c**2 * t), self.unranked_rd)

    def update_player(self, rating, rd, rating_opp, rd_opp, t, outcome):
        """Return the updated rating and RD of a player."""
        rd = self._update_rd(rd, t)
        valD = self._d(rating, rating_opp, rd_opp)

        new_rating = rating + self.q / (1 / rd**2 + 1 / valD) * self._g(rd_opp) * (outcome - self._E(rating, rating_opp, rd_opp))
        new_rd = math.sqrt(1 / (1 / rd**2 + 1 / valD))

        return (int(new_rating), max(int(new_rd), self.min_rd))
