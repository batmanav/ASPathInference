from dbmanager import DatabaseManager, MyDatabaseManager
from collections import Counter, deque

def baseAS(prefix):
	# db = DatabaseManager('test.sqlite')
	db = MyDatabaseManager()	

	allAS = set()
	result = db.query('SELECT ASes FROM test WHERE prefix = "%s"' % (prefix))
	for row in result:
		for i in row[0].split():
			allAS.add(i)
	return list(allAS)

def initpath(prefix):
	# db = DatabaseManager('test.sqlite')	
	db = MyDatabaseManager()	


	db.query('CREATE TABLE IF NOT EXISTS Manav (autos text, uncertainty int, frequency int, pathlength int, actualpath varchar(255) UNIQUE)') # % (prefix))

 	insertvalues = []
	result = db.query('SELECT ASes FROM test WHERE prefix = "%s"' % (prefix))
	for row in result:
		startingpath = " ".join(row[0].split()[::-1])
		temp = startingpath.split(' ')
		x = 0
		while x < len(temp):
			buf = ' '.join(temp[:x+1])
			# insertvalues.append('INSERT OR IGNORE INTO "%s" VALUES ("%s", 0, 0, 0, "%s")' % (prefix, buf.split(' ')[-1], buf))
			insertvalues.append('INSERT IGNORE INTO Manav VALUES ("%s", 0, 0, 0, "%s")' % (buf.split(' ')[-1], buf))
			x += 1

	for i in insertvalues:
		db.query(i)

def frequency(prefix):
	# db = DatabaseManager('test.sqlite')
	db = MyDatabaseManager()	



	result = db.query('SELECT ASes FROM test WHERE prefix = "%s"' % (prefix))

	rows = []

	for row in result:
		rows.append(row[0])

	# newresult = db.query('SELECT actualpath FROM "%s"' % (prefix))
	newresult = db.query('SELECT actualpath FROM Manav') # % (prefix))
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
		# todo.append('UPDATE "%s" SET frequency = %d WHERE actualpath = "%s"' % (prefix, freq, " ".join(apaths.split(' ')[::-1])))
		todo.append('UPDATE Manav SET frequency = %d WHERE actualpath = "%s"' % (freq, " ".join(apaths.split(' ')[::-1])))

	for i in todo:
		db.query(i)

def pathlength(prefix):
	# db = DatabaseManager('test.sqlite')	
	db = MyDatabaseManager()	

	# result = db.query('SELECT actualpath FROM "%s"' % (prefix))
	result = db.query('SELECT actualpath FROM Manav') # % (prefix))
	todo = []
	for row in result:
		pathl = len(row[0].split())
		todo.append('UPDATE Manav SET pathlength = %d WHERE actualpath = "%s"' % (pathl, row[0]))

	for i in todo:
		db.query(i)

def pathinference(prefix, baseAS):
	q = deque(baseAS)
	# db = DatabaseManager('test.sqlite')
	db = MyDatabaseManager()	

	while len(q) > 0:
		current_as = q.popleft()
		peers_of_current_as = getpeers(current_as)

		for peer in peers_of_current_as:

			if peer in baseAS:
				continue

			tpath = SPF(current_as, prefix)
			path = tpath[0]
			ul = tpath[1]
			pl = tpath[2]
			freq = tpath[3]

			valleyfree = 0
			#Check between peer and path if valleyfree.
			if pl > 1:
				s1 = db.query('SELECT relationship from caidarel WHERE AS1 = "%s" and AS2 = "%s"' % (path.split()[-2], path.split()[-1]))
				s2 = db.query('SELECT relationship from caidarel WHERE AS2 = "%s" and AS1 = "%s"' % (path.split()[-2], path.split()[-1]))
				rel = 0
				if s2 == -1:
					rel = 1
				elif s2 == 0 or s1 == 0:
					rel = 2
				elif s1 == -1:
					rel = 0

				if rel == 0:
					s1 = db.query('SELECT relationship from caidarel WHERE AS1 = "%s" and AS2 = "%s"' % (peer, path.split()[-1]))
					s2 = db.query('SELECT relationship from caidarel WHERE AS2 = "%s" and AS1 = "%s"' % (peer, path.split()[-1]))
					if s1 == -1 or s1 == 0:
						valleyfree = 1
					elif s2 == -1 or s2 == 0:
						valleyfree = 1
				elif rel == 1:
					s1 = db.query('SELECT relationship from caidarel WHERE AS1 = "%s" and AS2 = "%s"' % (peer, path.split()[-1]))
					if s1 == -1:
						valleyfree = 1		
				elif rel == 2:
					s1 = db.query('SELECT relationship from caidarel WHERE AS1 = "%s" and AS2 = "%s"' % (peer, path.split()[-1]))
					if s1 == -1:
						valleyfree = 1
			else:
				s1 = db.query('SELECT relationship from caidarel WHERE AS1 = "%s" and AS2 = "%s"' % (peer, path.split()[-1]))
				s2 = db.query('SELECT relationship from caidarel WHERE AS2 = "%s" and AS1 = "%s"' % (peer, path.split()[-1]))
				if s2 == 0 or s2 == -1:
					valleyfree = 1
				if s1 == 0 or s1 == -1:
					valleyfree = 1

			if not valleyfree:
				continue

			temp_best = SPF(peer, prefix)

			if temp_best[0] == -1:
				add2q = 0
			else:
				add2q = 1

			inserted = insertpath(path, peer, ul+1, pl+1, freq, prefix)

			if add2q == 1 and temp_best[0] != inserted and peer not in q and temp_best != -1:
				q.append(peer)

def getpeers(AS):
	peers = set()
	# db = DatabaseManager('test.sqlite')
	db = MyDatabaseManager()	

	result = db.query('SELECT AS1 from caidarel WHERE AS2 = "%s"' % (AS))
	for row in result:
		peers.add(row[0])
	result = db.query('SELECT AS2 from caidarel WHERE AS1 = "%s"' % (AS))
	for row in result:
		peers.add(row[0])
	return peers

def insertpath(path, peer, uncertainty, pathlength, freq, prefix):
	# db = DatabaseManager('test.sqlite')
	db = MyDatabaseManager()	

	newpath = str(path) + " " + peer
	# print peer, uncertainty, freq, pathlength, newpath
	# result = db.query('INSERT OR IGNORE INTO "%s" VALUES ("%s", %d, %d, %d, "%s")' % (prefix, peer, uncertainty, freq, pathlength, newpath))
	result = db.query('INSERT IGNORE INTO Manav VALUES ("%s", %d, %d, %d, "%s")' % (peer, uncertainty, freq, pathlength, newpath))
	return newpath

def SPF(AS, prefix):
	# db = DatabaseManager('test.sqlite')
	db = MyDatabaseManager()	


	# result = db.query('SELECT actualpath, uncertainty, pathlength, frequency FROM "%s" WHERE autos = "%s" ORDER BY pathlength, uncertainty DESC, frequency LIMIT 1' % (prefix, AS))
	result = db.query('SELECT actualpath, uncertainty, pathlength, frequency FROM Manav WHERE autos = "%s" ORDER BY pathlength, uncertainty DESC, frequency LIMIT 1' % (AS))
	bestpath = []
	for row in result:
		bestpath.append(row[0])
		bestpath.append(row[1])
		bestpath.append(row[2])
		bestpath.append(row[3])
		return bestpath
	else:
		return [-1]

def LUF(AS, prefix):
	# db = DatabaseManager('test.sqlite')	
	db = MyDatabaseManager()
	result = db.query('SELECT actualpath, uncertainty, pathlength, frequency FROM "%s" WHERE autos = "%s" ORDER BY uncertainty DESC, frequency, pathlength LIMIT 1' % (prefix, AS))
	bestpath = []
	for row in result:
		bestpath.append(row[0])
		bestpath.append(row[1])
		bestpath.append(row[2])
		bestpath.append(row[3])
		return bestpath
	else:
		return [-1]


