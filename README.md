
## AS Path Inference


---------


### Installation

---------
Prerequisites:

 - Python 2.7
 - sqlite3

#####CAIDA AS Relationship Database:

Get the as-rel file from: http://data.caida.org/datasets/as-relationships/serial-1/
The as-rel files contain p2p and p2c relationships.  The format is:

    <provider-as>|<customer-as>|-1

    <peer-as>|<peer-as>|0

To import this file into the database, update the filename in the caidarel.py file in the migrations folder, and then run caidarel.py. 


#####RIBS:
RIBS are taken from http://archive.routeviews.org/
Files:

1. ./routeviews-urls.list : List of URL of collectors(currently 18) available at archive.routeviews.org

2. ./getribs.py : 
Usage: python ./getribs.py
Get rib files from http://archive.routeviews.org for the urls specifies in routeviews-urls.list
Modify time,day,year,month parameters to get RIB of that time. 
RIBS are downloaded in 18 folders named by their respective numbers.

3. ./decompress_ribs.py :
Usage: python decompress_ribs.py from_folder to_folder
Decompress RIBS downloaded in folder beginning from_folder  to to_folder

4. ./generate_txt.py
Usage: python generate_txt.py from_folder to_folder
Generated txt file of RIBS from decompressed RIBS beginning from_folder  to to_folder
NOTE: Needs ./zebra-dump-parser in directory.

5. ./zebra-dump-parser

Steps:

1. Run python ./getribs.py

2. Run python decompress_ribs.py from_folder to_folder. Decompression may take time. Divide tasks in small range of 
from_folder to_folder

3. Run python generate_txt.py from_folder to_folder

4. After this txt RIB files are created in respective folders. use cat to combine all files in a single file
eg. cat ./1/RIB21.txt ./2/RIB21.txt ... ./18/RIB21.txt > ribout.txt

After generating ribout.txt:

- Run sortfile.py from migrations folder after changing to filename in sortfile.py


### Usage

---------
Clone the repo

Usage: `python pathinference.py <prefix>`

Using directly from the database:

- Load the database using: sqlite3 test.db
- '.tables' to view all tables



--------
Link to the paper: http://rio.ecs.umass.edu/mnilpub/papers/aspath_tech.pdf
