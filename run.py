from pymongo import MongoClient
import db

client = MongoClient(db.conn_string)
db = client.oscar

results = []

# find all nominees
for data in db.oscar_nominations.find():

	# loop cateogories
	for key in data:

		if key == "BEST PICTURE":

			# loop nominees
			for nominee in data[key]:

				item = [str(data["_id"]), key, nominee["name"], str(nominee["won"])]
				

				boxOfficeData = db.boxoffice_movies.find_one({"name": nominee["name"]})
				if boxOfficeData:

					# calculate days till the end of the year
					approxDaysItRan = 365 - boxOfficeData["release"].timetuple().tm_yday

					item.append(str(boxOfficeData["totalGross"]))
					item.append(str(approxDaysItRan))
					item.append(str(boxOfficeData["release"]))
				else:
					item.append("")
					item.append("")
					item.append("")

				results.append(item)

for row in results:
	line = ""

	for cell in row:
		line += cell + ";"

	print line
