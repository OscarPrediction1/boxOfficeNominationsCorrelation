from pymongo import MongoClient
import db

client = MongoClient(db.conn_string)
db = client.oscar

# find all nominees
for data in db.oscar_nominations.find():

	# process a single year
	print "Jahr", data["_id"]
	print ""

	# loop cateogories
	for key in data:

		if key == "BEST PICTURE":

			print "\t", key

			# loop nominees
			for nominee in data[key]:

				if(nominee["won"]):
					print "\t\t", nominee["name"], u"\U0001F3C6"
				else:
					print "\t\t", nominee["name"]
