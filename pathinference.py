from dbmanager import DatabaseManager
from utility import *
import sys

if __name__ == '__main__':

	if len(sys.argv) < 2:
		print "Usage: python pathinference.py <prefix>"
		exit()
	else:
		prefix = sys.argv[1]

	print "Running for prefix: ", prefix

	allAS = baseAS(prefix)
	initpath(prefix)
	frequency(prefix)
	pathlength(prefix)
	pathinference(prefix, allAS)