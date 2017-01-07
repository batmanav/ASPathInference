import sqlite3

conn = sqlite3.connect('test.sqlite')
c = conn.cursor()

c.execute('CREATE TABLE test (prefix text, ASes text)')
col1 = 'prefix'
col2 = 'ASes'
with open("import.txt") as f:
	for line in f:
		temp = line.split(' ', 1)
		print temp[0], temp[1].strip('\n')
		c.execute("INSERT INTO test (prefix, ASes) VALUES ('{pp}', '{lol}')".format(pp=str(temp[0]), lol=str(temp[1].strip('\n'))))

# conn.commit()


conn.commit()
conn.close()

