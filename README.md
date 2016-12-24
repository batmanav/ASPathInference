
## AS Path Inference


----------


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

To import this file into the database, update the filename in the caidarel.py file in the migrations folder run the file. 


#####RIBS:



### Usage

---------
Clone the repo

Usage: `python pathinference.py <prefix>`



--------
Link to the paper: http://rio.ecs.umass.edu/mnilpub/papers/aspath_tech.pdf
