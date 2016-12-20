import sqlite3

conn = sqlite3.connect('../test.sqlite')
c = conn.cursor()

c.execute('CREATE TABLE caidarel (AS1 text, AS2 text, relationship number)')
col1 = 'AS1'
col2 = 'AS2'
with open("caidarel.txt") as f:
	for line in f:
		temp = line.split(' ')
		# print temp[0], temp[1].strip('\n')
		c.execute("INSERT INTO caidarel (AS1, AS2, relationship) VALUES ('{pp}', '{lol}', '{x}')".format(pp=str(temp[0]), lol=str(temp[1]), x=str(temp[2])))

# conn.commit()


conn.commit()
conn.close()

