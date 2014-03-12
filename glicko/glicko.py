import math

c = 17.5

def q():
	return math.log(10) / 400

def g(rd):
	return 1 / math.sqrt(1 + 3 * q() ** 2 * rd ** 2 / math.pi ** 2)

def E(rating, rating_opp, rd_opp):
	return 1 / (1 + 10 ** (-g(rd_opp) * (rating - rating_opp) / 400))

def d(rating, rating_opp, rd_opp):
	valE = E(rating, rating_opp, rd_opp)
	return 1 / (q() ** 2 * g(rd_opp) ** 2 * valE * (1 - valE))

def update_rd(rd_old, t):
	return min(math.sqrt(rd_old ** 2 + c ** 2 * t), 350)

def update_player(rating, rd, rating_opp, rd_opp, t, outcome):
	rd = update_rd(rd, t)
	valD = d(rating, rating_opp, rd_opp)

	new_rating = rating + q() / (1 / rd ** 2 + 1 / valD) * g(rd_opp) * (outcome - E(rating, rating_opp, rd_opp))
	new_rd = math.sqrt(1 / (1 / rd ** 2 + 1 / valD))

	return (int(new_rating), int(new_rd))