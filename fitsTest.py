from fits import app, db
from utils import makeId, getHash
import json

session = db.session

USERNAME = "davish20"
FIRST = "Hananiah"
LAST = "Davis"
PASSWORD = "ballislife"

print("################    DB TESTS   ###################")
# Provided DB tests
## No buckets to begin with
assert(len(db.getUsers()) == 0)
## Adding a user
db.addUser()
