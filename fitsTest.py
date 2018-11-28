from fits import app, db
from utils import makeId, getHash
import json

session = db.session

USERNAME = "davish20"
FIRST = "Hananiah"
LAST = "Davis"
PASSWORD = getHash("ballislife")
ID = 1
TYPE_NAME = "Email"
ID_LOCATION = 2
LOCATION_NAME = "Science Center"
ID2 = 3
TYPE_NAME2 = "Phone"

## ADD MORE TYPES AND LOCATIONS FOR TESTS ##

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

## Re-adding type for further tests
type = db.addType(id = ID, name = TYPE_NAME)

## No location to begin with
assert(len(db.getLocations()) == 0)

## Adding a type
db.addLocation(id = ID_LOCATION, name = LOCATION_NAME)
assert(len(db.getLocations()) == 1)
location = db.getLocation(ID_LOCATION)
assert(location is not None)
assert(location.id == ID_LOCATION)
assert(location.name == LOCATION_NAME)
assert(db.getLocation(ID_LOCATION + 3) is None)
assert(db.getLocations()[0] is location)
db.commit()

## Deleting the type
db.deleteLocation(location)
location = db.getLocation(LOCATION_NAME)
assert(location is None)
db.commit()

## Re-adding location for further tests
location = db.addLocation(id = ID_LOCATION, name = LOCATION_NAME)

## Adding an issue
db.addIssue(id = ID2, userId = USERNAME, type = TYPE_NAME2 , location = LOCATION_NAME)
assert(len(db.getIssues()) == 1)
issue = db.getIssue(id = ID2)
assert(issue is not None)
assert(issue.id == ID2)
assert(issue.userId == USERNAME)
assert(issue.type == TYPE_NAME2)
assert(issue.location == LOCATION_NAME)
assert(db.getIssue(ID2 + 10) is None)
assert(db.getIssues()[0] is issue)
db.commit()

## Deleting the issue
db.deleteIssue(issue)
issue = db.getIssue(ID2)
assert(issue is None)
db.commit()

## Readding the issue for further tests
issue = db.addIssue(id = ID2, userId = USERNAME, type = TYPE_NAME2 , location = LOCATION_NAME)


print("################ DB TESTS DONE ###################")
# Provided API tests
print("################   API TESTS   ###################")

app.config['TESTING'] = True
client = app.test_client()
#testing the user_list funciton
r = client.get('/user')
assert(r.status_code == 200)
assert(len(r.json['users']) == 1)
assert("users" in r.json and "link" in r.json["users"][0] and "username" in r.json["users"][0] and "first" in r.json['users'][0] and "last" in r.json['users'][0])
assert(r.json['users'][0]["username"] == "davish20")
assert(r.json['users'][0]["last"] == "Davis")
#testing the find_user function
r = client.get('/user/davish20?password=ballislife')
assert(r.status_code == 200)
assert(r.json['username'] == "davish20")
assert(r.json['first'] == 'Hananiah')
assert(r.json['last'] == 'Davis')
assert(len(r.json['issues']) == 1)
assert(r.json['link'] == '/user/davish20')
r = client.get('/user/davish20')
assert(r.status_code == 403)
assert(r.json['error'] == 'must provide a password parameter')
r = client.get('/user/davish20?password=runningislife')
assert(r.status_code == 403)
assert(r.json['error'] == "Incorrect password.")
r = client.get('/user/hedrickj19?password=run')
assert(r.status_code == 404)
assert(r.json['error'] == "username not found in the database")