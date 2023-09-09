from pymongo import MongoClient

# TODO: move to env file
mongopass = "mongodb+srv://root:gichackathon2023@gichackathon2023.xxk3lqm.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(mongopass)
db = client.GICHackathon2023