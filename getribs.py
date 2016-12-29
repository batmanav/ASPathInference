# Get rib files from http://archive.routeviews.org for the urls specifies in routeviews-urls.txt
import urllib
import urllib2
import requests
import os

# Modify these 4 parameters to get RIBS for different time.
month='07' # month to get ribs of.
year='2016' # year to get ribs of.
time='0600' # time of ribs collection
DAY_OF_MONTH=20 # day of rib collection
# url = 'http://archive.routeviews.org/route-views.kixp/bgpdata/2016.07/RIBS/rib.20160701.1200.bz2'


DAY_STR=['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']

# File containting URL of path collectors
URLS = './routeviews-urls.txt'


with open(URLS) as f:
    routeviewsurls = f.readlines()

folder_no=1;

for baseurl in routeviewsurls:
	
	folder_path='./'+str(folder_no)+'/'
	folder_no=folder_no+1

	if not os.path.exists(folder_path):
		os.makedirs(folder_path)
	
	baseurl=baseurl.rstrip()
	ribsurl=baseurl+'/'+year+'.'+month+'/RIBS/rib.'+year+month

	day=DAY_OF_MONTH
	downloadurl=ribsurl+DAY_STR[day]+'.'+time+'.bz2'
        print "dowloading "+downloadurl+' ...'
        save_path=folder_path+'RIB'+DAY_STR[day]+'.bz2'
        urllib.urlretrieve(downloadurl, save_path)
        print 'done'
        print save_path+"\n"


