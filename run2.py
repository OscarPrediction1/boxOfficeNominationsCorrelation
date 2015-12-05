from pymongo import MongoClient
import db, sys, pymongo
import os, json, requests, urllib, calendar, time
from datetime import datetime

client = MongoClient(db.conn_string)
db = client.oscar

sep = ";"

results = [["year","name","won","gross","gross per day","playdays in year","release date"]]

# find all nominees
for data in db.oscar_nominations_extended.find():

	if data["film"]:

		boxOfficeData = None

		try:

			# fetch boxOfficeId
			url_params = urllib.urlencode({"movie": data["film"], "year": str(data["year"])})
			resp = requests.get(url="http://boxofficeid.thomasbrueggemann.com/?" + url_params)
			boxOfficeData = json.loads(resp.text)

			if len(boxOfficeData) == 1:
				boxOfficeData = boxOfficeData[0]

				boxOfficeData["release"] = datetime.strptime(boxOfficeData["release"], "%Y-%m-%dT%H:%M:%S.000Z")

				boxOfficeData = boxOfficeData = db.boxoffice_movies.find_one({"boxOfficeId": boxOfficeData["boxOfficeId"]})

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
				result += boxOfficeData["boxOfficeId"] + sep
				
				if data["won"] == True:
					result += "1" + sep
				else:
					result += "0" + sep

				result += gross + sep
				result += grossPerDate + sep
				result += playDays + sep + releaseDate

				print result
		except:
			pass