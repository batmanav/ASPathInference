from dbmanager import DatabaseManager
from collections import Counter, deque

def baseAS(prefix):
	db = DatabaseManager('test.sqlite')
	allAS = set()
	result = db.query('SELECT ASes FROM test WHERE prefix = "%s"' % (prefix))
	for row in result:
		for i in row[0].split():
			allAS.add(i)
	return list(allAS)

def initpath(prefix):
	db = DatabaseManager('test.sqlite')	

	# result = db.query('SELECT count(*) FROM sqlite_master WHERE type="table" AND name="%s";' % (prefix))
	# iftable = 0
	# for i in result:
	# 	iftable = i[0]
	# if iftable == 0:
	# print "Creating a table for this prefix"

	db.query('CREATE TABLE IF NOT EXISTS "%s" (autos text, uncertainty integer, frequency integer , pathlength integer, actualpath text UNIQUE)' % (prefix))

 	insertvalues = []
	result = db.query('SELECT ASes FROM test WHERE prefix = "%s"' % (prefix))
	for row in result:
		startingpath = " ".join(row[0].split()[::-1])
		temp = startingpath.split(' ')
		x = 0
		while x < len(temp):
			buf = ' '.join(temp[:x+1])
			insertvalues.append('INSERT OR IGNORE INTO "%s" VALUES ("%s", 0, 0, 0, "%s")' % (prefix, buf.split(' ')[-1], buf))
			# db.query('INSERT INTO "%s" VALUES ("%s", 0, 0, 0, "%s")' % (prefix, buf.split(' ')[-1], buf))
			x += 1

	for i in insertvalues:
		db.query(i)
		# x = 0
		# temp = startingpath.split(' ')
		# while x < temp:
		# 	print startingpath[:x]
		# 	x += 1
		# print row[0].split(' ').reverse().join(' ')

def frequency(prefix):
	db = DatabaseManager('test.sqlite')

	result = db.query('SELECT ASes FROM test WHERE prefix = "%s"' % (prefix))
	rows = []

	for row in result:
		rows.append(row[0])

	newresult = db.query('SELECT actualpath FROM "%s"' % (prefix))
	allpaths = []
	for row in newresult:
		allpaths.append(" ".join(row[0].split(' ')[::-1]))

	todo = []

	for apaths in allpaths:
		freq = 0
		for path in rows:
			i = path.split(' ')
			j = apaths.split(' ')
			# print Counter(i), '+', Counter(j), (Counter(i) - Counter(j))
			if not Counter(j) - Counter(i):
				freq += 1
		todo.append('UPDATE "%s" SET frequency = %d WHERE actualpath = "%s"' % (prefix, freq, " ".join(apaths.split(' ')[::-1])))
		# print freq

	for i in todo:
		db.query(i)

def pathlength(prefix):
	db = DatabaseManager('test.sqlite')
	result = db.query('SELECT actualpath FROM "%s"' % (prefix))

	paths = []
	todo = []
	for row in result:
		pathl = len(row[0].split())
		todo.append('UPDATE "%s" SET pathlength = %d WHERE actualpath = "%s"' % (prefix, pathl, row[0]))

	for i in todo:
		db.query(i)

def pathinference(prefix, baseAS):
	q = deque(baseAS)
	while len(q) > 0:
		autos = q.pop()
		db.query('CREATE TABLE IF NOT EXISTS "%s" (peers text UNIQUE)' % (autos))
		peers = db.query('SELECT peers FROM "%s"' % (autos))
		if not peers:
			updatepeers()
		peers = db.query('SELECT peers FROM "%s"' % (autos))
		allpeers = []
		for i in peers:
			allpeers.append(i)
		caidacheck = False
		for peer in allpeers:
			bestpath = db.query('SELECT actualpath FROM "%s" ORDER BY pathlength, frequency LIMIT 1')
			path = bestpath.split(' ')
			relationship = db.query('SELECT relationship FROM caidarel WHERE as1 = "%s" and as2 ="%s" OR as1 = "%s" and as2 ="%s"' % (path[-1], path[-2], paht[-2], path[-1]))
			#Complete checking valleyfree
			if relationship == 0:
				newrelationship = db.query('SELECT relationship FROM caidarel WHERE as1 = "%s" and as2 ="%s" OR as1 = "%s" and as2 ="%s"' % (path[-1], peer, peer, path[-1]))
			elif relationship == 1:
				newrelationship = db.query('SELECT relationship FROM caidarel WHERE as1 = "%s" and as2 ="%s" OR as1 = "%s" and as2 ="%s"' % (path[-1], peer, peer, path[-1]))
			elif relationship == -1:
				newrelationship = db.query('SELECT relationship FROM caidarel WHERE as1 = "%s" and as2 ="%s" OR as1 = "%s" and as2 ="%s"' % (path[-1], peer, peer, path[-1]))
				
			if caidacheck == True:
				print "CAIDA checked"

			bestpath = db.query('SELECT actualpath FROM "%s" ORDER BY pathlength, frequency LIMIT 1')

			if peer in baseAS and peer not in path:
				#check origin



		#TODO Import from caidarel

	# print "Hey"


#TODO

def updatepeers(AS):
	print "TODO"
	

