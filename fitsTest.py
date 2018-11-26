from fits import app, db
from utils import makeId, getHash
import json

session = db.session

USERNAME = "davish20"
FIRST = "Hananiah"
LAST = "Davis"
PASSWORD = "ballislife"
ID = 1
TYPE_NAME = "Email"

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

## No types to begin with
assert(len(db.getTypes()) == 0)

## Adding a type
db.addType(id = ID, name = TYPE_NAME)
assert(len(db.getTypes()) == 1)
type = db.getType(ID)
assert(type is not None)
assert(type.id == ID)
assert(type.name == TYPE_NAME)
assert(db.getType(ID + 3) is None)
assert(db.getTypes()[0] is type)
db.commit()

## Deleting the type
db.deleteType(type)
type = db.getType(TYPE_NAME)
assert(type is None)
db.commit()
