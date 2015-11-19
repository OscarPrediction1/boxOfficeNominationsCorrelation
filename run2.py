from pymongo import MongoClient
import db, sys

client = MongoClient(db.conn_string)
db = client.oscar

sep = ";"

results = [["year","name","won","gross","gross per day","playdays in year","release date"]]

# find all nominees
for data in db.oscar_nominations_extended.find():

	if data["film"]:

		boxOfficeDatas = db.boxoffice_movies.find({"name": data["film"]})

		for d in boxOfficeDatas:
			if d["release"].year == data["year"]:
				boxOfficeData = d

		if boxOfficeData:

			lastDay = None
			gross = ""
			grossPerDate = ""
			playDays = ""
			releaseDate = ""

			# find gross at the end of the year
			if "history" in boxOfficeData:
				lastDay = boxOfficeData["history"][-1]

			if lastDay:
				gross = str(lastDay["grossToDate"])
				grossPerDate = str(int(lastDay["grossToDate"] / int(lastDay["dayNumber"])))
				playDays = str(lastDay["dayNumber"])
			
			releaseDate = str(boxOfficeData["release"])

		result = str(data["year"]) + sep
		result += data["film"] + sep
		
		if data["won"] == True:
			result += "1" + sep
		else:
			result += "0" + sep

		result += gross + sep
		result += grossPerDate + sep
		result += playDays + sep + releaseDate

		print result