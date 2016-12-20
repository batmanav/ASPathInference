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
			if not Counter(j) - Counter(i):
				freq += 1
		todo.append('UPDATE "%s" SET frequency = %d WHERE actualpath = "%s"' % (prefix, freq, " ".join(apaths.split(' ')[::-1])))

	for i in todo:
		db.query(i)

def pathlength(prefix):
	db = DatabaseManager('test.sqlite')
	result = db.query('SELECT actualpath FROM "%s"' % (prefix))
	todo = []
	for row in result:
		pathl = len(row[0].split())
		todo.append('UPDATE "%s" SET pathlength = %d WHERE actualpath = "%s"' % (prefix, pathl, row[0]))

	for i in todo:
		db.query(i)

def pathinference(prefix, baseAS):
	q = deque(baseAS)
	db = DatabaseManager('test.sqlite')

	while len(q) > 0:
		current_as = q.popleft()
		peers_of_current_as = getpeers(current_as)

		# Check if path is valley free

		for peer in peers_of_current_as:
			if peer in baseAS:
				continue
			# path, ul, pl = SPF(current_as, prefix)
			path = SPF(current_as, prefix)
			#Check between peer and path if valleyfree.
			valleyfree = 1
			temp_best = SPF(peer, prefix)
			ul = 0
			pl = 1
			print temp_best
			inserted = insertpath(path, peer, ul+1, pl+1)
			if temp_best != inserted and peer not in q and temp_best!=-1:
				q.append(peer)
				print q


def getpeers(AS):
	peers = set()
	db = DatabaseManager('test.sqlite')
	result = db.query('SELECT AS1 from caidarel WHERE AS2 = "%s"' % (AS))
	for row in result:
		peers.add(row[0])
	result = db.query('SELECT AS2 from caidarel WHERE AS1 = "%s"' % (AS))
	for row in result:
		peers.add(row[0])
	return peers

def insertpath(path, peer, uncertainty, pathlength):
	db = DatabaseManager('test.sqlite')
	print str(path) + " " + peer
	print uncertainty, pathlength
	# result = db.query()

def SPF(AS, prefix):
	db = DatabaseManager('test.sqlite')
	result = db.query('SELECT actualpath, uncertainty, pathlength FROM "%s" WHERE autos = "%s" ORDER BY pathlength, uncertainty DESC, frequency LIMIT 1' % (prefix, AS))
	bestpath = -1
	for row in result:
		bestpath = row[0]
		uncertainty = row[1]
		pathlength = row[2]
		break
	# if bestpath == -1:
	return bestpath
	# else:
		# return bestpath, uncertainty, pathlength

def LUF(AS, prefix):
	db = DatabaseManager('test.sqlite')
	result = db.query('SELECT actualpath FROM "%s" WHERE autos = "%s" ORDER BY uncertainty DESC, frequency, pathlength LIMIT 1' % (prefix, AS))
	bestpath = -1
	for row in result:
		bestpath = row[0]
		break
	return bestpath


