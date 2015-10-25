from pymongo import MongoClient
import db

client = MongoClient(db.conn_string)
db = client.oscar

# find all nominees
for data in db.oscar_nominations.find():

	# process a single year
	print "\n"
	print "Jahr", data["_id"]
	print ""

	# loop cateogories
	for key in data:

		if key == "BEST PICTURE":

			print "\t", key

			# loop nominees
			for nominee in data[key]:

				line = "\t\t" + nominee["name"]

				if(nominee["won"]):
					line += u" \U0001F3C6"

				boxOfficeData = db.boxoffice_movies.find_one({"name": nominee["name"]})
				if boxOfficeData:
					line += " $" + "{0:,}".format(boxOfficeData["totalGross"]).replace(",",".")

				print line
