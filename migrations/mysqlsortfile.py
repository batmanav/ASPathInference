import MySQLdb

db = MySQLdb.connect("localhost","root","manav","gao" )

c = db.cursor()

c.execute('CREATE TABLE IF NOT EXISTS test (prefix text, ASes text)')
col1 = 'prefix'
col2 = 'ASes'
with open("import.txt") as f:
	for line in f:
		temp = line.split(' ', 1)
		print temp[0], temp[1].strip('\n')
		c.execute("INSERT INTO test (prefix, ASes) VALUES ('{pp}', '{lol}')".format(pp=str(temp[0]), lol=str(temp[1].strip('\n'))))

db.commit()
db.close()