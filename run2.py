from pymongo import MongoClient
import db, sys, pymongo

client = MongoClient(db.conn_string)
db = client.oscar

sep = ";"

results = [["year","name","won","gross","gross per day","playdays in year","release date"]]

# find all nominees
for data in db.oscar_nominations_extended.find():

	if data["film"]:

		boxOfficeData = None
		boxOfficeDatas = db.boxoffice_movies.find({"name": data["film"]}).sort([("release", pymongo.ASCENDING)])

		for d in boxOfficeDatas:
			if d["release"].year == data["year"]:
				boxOfficeData = d

		gross = ""
		grossPerDate = ""
		playDays = ""
		releaseDate = ""

		if boxOfficeData:

			lastDay = None

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