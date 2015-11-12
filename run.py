from pymongo import MongoClient
import db

client = MongoClient(db.conn_string)
db = client.oscar

results = [["year","oscar","name","won","gross","gross per day","playdays in year","release date"]]

# find all nominees
for data in db.oscar_nominations.find():

	# loop cateogories
	for key in data:

		if key == "BEST PICTURE":

			# loop nominees
			for nominee in data[key]:

				item = [str(data["_id"]), key, nominee["name"].replace(",", ""), str(nominee["won"])]
				
				boxOfficeData = db.boxoffice_movies.find_one({"name": nominee["name"]})
				if boxOfficeData:

					# calculate days till the end of the year
					#approxDaysItRan = 365 - boxOfficeData["release"].timetuple().tm_yday

					lastDay = None

					# find gross at the end of the year
					if "history" in boxOfficeData:

						#for day in boxOfficeData["history"]:
						#	lastDay = day
						#
						#	if day["date"].day == 31 and day["date"].month == 12 and day["date"].year == boxOfficeData["release"].year:
						#		break
						lastDay = boxOfficeData["history"][-1]

					if lastDay:
						item.append(str(lastDay["grossToDate"]))
						item.append(str(int(lastDay["grossToDate"] / int(lastDay["dayNumber"]))))
						item.append(str(lastDay["dayNumber"]))
					else:
						item.append("")
						item.append("")
						item.append("")
					
					item.append(str(boxOfficeData["release"]))
				else:
					item.append("")
					item.append("")
					item.append("")
					item.append("")

				results.append(item)

for row in results:
	line = ""

	for cell in row:
		line += cell + ","

	print line
