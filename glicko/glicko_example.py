import datetime
import sqlite3
import glicko

def main():
	cur = init_db()
	update_players(cur)

	cur.execute('SELECT * FROM players')
	for row in cur:
		print(row['rating'])
		print(row['rd'])
		print(row['last_match'])

def init_db():
	con = sqlite3.connect(':memory:')
	con.row_factory = sqlite3.Row
	cur = con.cursor()
	cur.execute('PRAGMA foreign_keys = ON')

	cur.execute(
		'''CREATE TABLE players(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		rating INTEGER NOT NULL,
		rd INTEGER NOT NULL,
		last_match TEXT)''')

	cur.execute(
		'''CREATE TABLE matches(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		winner INTEGER NOT NULL,
		loser INTEGER NOT NULL,
		match_date TEXT NOT NULL,
		FOREIGN KEY(winner) REFERENCES players(id),
		FOREIGN KEY(loser) REFERENCES players(id))''')

	cur.execute('INSERT INTO players(rating, rd, last_match) VALUES(1400, 30, \'2014-03-01\')')
	cur.execute('INSERT INTO players(rating, rd, last_match) VALUES(1500, 200, \'2014-03-01\')')
	cur.execute('INSERT INTO players(rating, rd, last_match) VALUES(1550, 100, \'2014-03-01\')')
	cur.execute('INSERT INTO players(rating, rd, last_match) VALUES(1700, 300, \'2014-03-01\')')
	cur.execute('INSERT INTO matches(winner, loser, match_date) VALUES(2, 1, \'2014-03-10\')')
	cur.execute('INSERT INTO matches(winner, loser, match_date) VALUES(3, 2, \'2014-03-11\')')
	cur.execute('INSERT INTO matches(winner, loser, match_date) VALUES(4, 2, \'2014-03-12\')')

	return cur

def update_players(cur):
	cur.execute('SELECT * FROM matches ORDER BY match_date')
	matches = cur.fetchall()

	for match in matches:
		id_winner = match['winner']
		id_loser = match['loser']

		winner = cur.execute('SELECT * FROM players WHERE id = ?', (id_winner,)).fetchone()
		loser = cur.execute('SELECT * FROM players WHERE id = ?', (id_loser,)).fetchone()

		last_match_winner = datetime.datetime.strptime(winner['last_match'], '%Y-%m-%d').date()
		last_match_loser = datetime.datetime.strptime(loser['last_match'], '%Y-%m-%d').date()
		match_date = datetime.datetime.strptime(match['match_date'], '%Y-%m-%d').date()

		(rating_winner, rd_winner) = glicko.update_player(
			winner['rating'],
			winner['rd'],
			loser['rating'],
			loser['rd'],
			(match_date - last_match_winner).days,
			1)

		(rating_loser, rd_loser) = glicko.update_player(
			loser['rating'],
			loser['rd'],
			winner['rating'],
			winner['rd'],
			(match_date - last_match_loser).days,
			0)

		# Update both players in DB.
		cur.execute('UPDATE players SET rating = ?, rd = ?, last_match = ? WHERE id = ?', (rating_winner, rd_winner, match['match_date'], id_winner))
		cur.execute('UPDATE players SET rating = ?, rd = ?, last_match = ? WHERE id = ?', (rating_loser, rd_loser, match['match_date'], id_loser))

		# Delete match from DB.
		cur.execute('DELETE FROM matches WHERE id = ?', (match['id'],))

if __name__ == '__main__':
	main()
