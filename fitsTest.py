from fits import app, db
from utils import makeId, getHash
import json

session = db.session

USERNAME = "davish20"
FIRST = "Hananiah"
LAST = "Davis"
PASSWORD = "ballislife"

print("################    DB TESTS   ###################")
## No user to begin with
assert(len(db.getUsers()) == 0)

## Adding a user
db.addUser(username = USERNAME, first = FIRST, last = LAST, password = PASSWORD)
assert(len(db.getUsers()) == 1)
user = db.getUser(USERNAME)
assert(user is not None)
assert(user.username == USERNAME)
assert(user.password == PASSWORD)
assert(user.first == FIRST)
assert(user.last == LAST)
assert(db.getUser(USERNAME + "pigcow") is None)
assert(db.getUsers()[0] is user)
db.commit()

## Deleting the user
db.deleteUser(user)
user = db.getUser(USERNAME)
assert(user is None)
db.commit()

## Re-adding user for further tests
user = db.addUser(username = USERNAME, first = FIRST, last = LAST, password = PASSWORD)
