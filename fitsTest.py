from fits import app, db
from utils import makeId, getHash
import json

session = db.session

USERNAME = "davish20"
FIRST = "Hananiah"
LAST = "Davis"
PASSWORD = getHash("ballislife")
USERNAME2 = "monnine20"
FIRST2 = "Ethan"
LAST2 = "Monnin"
PASSWORD2 = getHash("poleislife")
USERNAME3 = "mundth19"
FIRST3 = "Hannah"
LAST3 = "Mundt"
PASSWORD3 = getHash("laxislife")
USERNAME4 = "caldwellp20"
FIRST4 = "Paxton"
LAST4 = "Caldwell"
PASSWORD4 = getHash("javislife")
ID_TYPE = 1
ID_TYPE2 = 2
ID_TYPE3 = 3
ID_TYPE4 = 4
TYPE_NAME = "Email"
TYPE_NAME2 = "Phone"
TYPE_NAME3 = "Laptop"
TYPE_NAME4 = "Classroom"
ID_LOCATION = 5
ID_LOCATION2 = 6
ID_LOCATION3 = 7
ID_LOCATION4 = 8
LOCATION_NAME = "Science Center"
LOCATION_NAME2 = "Classic Hall"
LOCATION_NAME3 = "Library"
LOCATION_NAME4 = "CFA"
ID_ISSUE = 9
ID_ISSUE2 = 10
ID_ISSUE3 = 11
ID_ISSUE4 = 12

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
db.addType(id = ID_TYPE, name = TYPE_NAME)
assert(len(db.getTypes()) == 1)
type = db.getType(ID_TYPE)
assert(type is not None)
assert(type.id == ID_TYPE)
assert(type.name == TYPE_NAME)
assert(db.getType(ID_TYPE + 1000) is None)
assert(db.getTypes()[0] is type)
db.commit()

## Deleting the type
db.deleteType(type)
type = db.getType(TYPE_NAME)
assert(type is None)
db.commit()

## Re-adding type for further tests
type = db.addType(id = ID_TYPE, name = TYPE_NAME)

## No location to begin with
assert(len(db.getLocations()) == 0)

## Adding a location
db.addLocation(id = ID_LOCATION, name = LOCATION_NAME)
assert(len(db.getLocations()) == 1)
location = db.getLocation(ID_LOCATION)
assert(location is not None)
assert(location.id == ID_LOCATION)
assert(location.name == LOCATION_NAME)
assert(db.getLocation(ID_LOCATION + 3) is None)
assert(db.getLocations()[0] is location)
db.commit()

## Deleting the location
db.deleteLocation(location)
location = db.getLocation(LOCATION_NAME)
assert(location is None)
db.commit()

## Re-adding location for further tests
location = db.addLocation(id = ID_LOCATION, name = LOCATION_NAME)

## Adding an issue
db.addIssue(id = ID_ISSUE, userId = USERNAME, type = TYPE_NAME , location = LOCATION_NAME)
assert(len(db.getIssues()) == 1)
issue = db.getIssue(id = ID_ISSUE)
assert(issue is not None)
assert(issue.id == ID_ISSUE)
assert(issue.userId == USERNAME)
assert(issue.type == TYPE_NAME)
assert(issue.location == LOCATION_NAME)
assert(db.getIssue(ID_ISSUE + 1000) is None)
assert(db.getIssues()[0] is issue)
db.commit()

## Deleting the issue
db.deleteIssue(issue)
issue = db.getIssue(ID_ISSUE)
assert(issue is None)
db.commit()

## Readding the issue for further tests
issue = db.addIssue(id = ID_ISSUE, userId = USERNAME, type = TYPE_NAME , location = LOCATION_NAME)

#############################################################

## Adding a second user
db.addUser(username = USERNAME2, first = FIRST2, last = LAST2, password = PASSWORD2)
assert(len(db.getUsers()) == 2)
user = db.getUser(USERNAME2)
assert(user is not None)
assert(user.username == USERNAME2)
assert(user.password == PASSWORD2)
assert(user.first == FIRST2)
assert(user.last == LAST2)
assert(db.getUser(USERNAME2 + "pigcow") is None)
assert(db.getUsers()[1] is user)
db.commit()

## Adding a second type
db.addType(id = ID_TYPE2, name = TYPE_NAME2)
assert(len(db.getTypes()) == 2)
type = db.getType(ID_TYPE2)
assert(type is not None)
assert(type.id == ID_TYPE2)
assert(type.name == TYPE_NAME2)
assert(db.getType(ID_TYPE2 + 1000) is None)
assert(db.getTypes()[1] is type)
db.commit()

## Adding a second location
db.addLocation(id = ID_LOCATION2, name = LOCATION_NAME2)
assert(len(db.getLocations()) == 2)
location = db.getLocation(ID_LOCATION2)
assert(location is not None)
assert(location.id == ID_LOCATION2)
assert(location.name == LOCATION_NAME2)
assert(db.getLocation(ID_LOCATION2 + 1000) is None)
assert(db.getLocations()[1] is location)
db.commit()

## Adding a second issue
db.addIssue(id = ID_ISSUE2, userId = USERNAME2, type = TYPE_NAME2 , location = LOCATION_NAME2)
assert(len(db.getIssues()) == 2)
issue = db.getIssue(id = ID_ISSUE2)
assert(issue is not None)
assert(issue.id == ID_ISSUE2)
assert(issue.userId == USERNAME2)
assert(issue.type == TYPE_NAME2)
assert(issue.location == LOCATION_NAME2)
assert(db.getIssue(ID_ISSUE2 + 1000) is None)
assert(db.getIssues()[1] is issue)
db.commit()

#########################################################

## Adding a third user
db.addUser(username = USERNAME3, first = FIRST3, last = LAST3, password = PASSWORD3)
assert(len(db.getUsers()) == 3)
user = db.getUser(USERNAME3)
assert(user is not None)
assert(user.username == USERNAME3)
assert(user.password == PASSWORD3)
assert(user.first == FIRST3)
assert(user.last == LAST3)
assert(db.getUser(USERNAME3 + "pigcow") is None)
assert(db.getUsers()[2] is user)
db.commit()

## Adding a third type
db.addType(id = ID_TYPE3, name = TYPE_NAME3)
assert(len(db.getTypes()) == 3)
type = db.getType(ID_TYPE3)
assert(type is not None)
assert(type.id == ID_TYPE3)
assert(type.name == TYPE_NAME3)
assert(db.getType(ID_TYPE3 + 1000) is None)
assert(db.getTypes()[2] is type)
db.commit()

## Adding a third location
db.addLocation(id = ID_LOCATION3, name = LOCATION_NAME3)
assert(len(db.getLocations()) == 3)
location = db.getLocation(ID_LOCATION3)
assert(location is not None)
assert(location.id == ID_LOCATION3)
assert(location.name == LOCATION_NAME3)
assert(db.getLocation(ID_LOCATION3 + 1000) is None)
assert(db.getLocations()[2] is location)
db.commit()

## Adding a third issue
db.addIssue(id = ID_ISSUE3, userId = USERNAME3, type = TYPE_NAME3 , location = LOCATION_NAME3)
assert(len(db.getIssues()) == 3)
issue = db.getIssue(id = ID_ISSUE3)
assert(issue is not None)
assert(issue.id == ID_ISSUE3)
assert(issue.userId == USERNAME3)
assert(issue.type == TYPE_NAME3)
assert(issue.location == LOCATION_NAME3)
assert(db.getIssue(ID_ISSUE3 + 1000) is None)
assert(db.getIssues()[2] is issue)
db.commit()

##############################################################

## Adding a fourth user
db.addUser(username = USERNAME4, first = FIRST4, last = LAST4, password = PASSWORD4)
assert(len(db.getUsers()) == 4)
user = db.getUser(USERNAME4)
assert(user is not None)
assert(user.username == USERNAME4)
assert(user.password == PASSWORD4)
assert(user.first == FIRST4)
assert(user.last == LAST4)
assert(db.getUser(USERNAME4 + "pigcow") is None)
assert(db.getUsers()[3] is user)
db.commit()

## Adding a fourth type
db.addType(id = ID_TYPE4, name = TYPE_NAME4)
assert(len(db.getTypes()) == 4)
type = db.getType(ID_TYPE4)
assert(type is not None)
assert(type.id == ID_TYPE4)
assert(type.name == TYPE_NAME4)
assert(db.getType(ID_TYPE4 + 1000) is None)
assert(db.getTypes()[3] is type)
db.commit()

## Adding a fourth location
db.addLocation(id = ID_LOCATION4, name = LOCATION_NAME4)
assert(len(db.getLocations()) == 4)
location = db.getLocation(ID_LOCATION4)
assert(location is not None)
assert(location.id == ID_LOCATION4)
assert(location.name == LOCATION_NAME4)
assert(db.getLocation(ID_LOCATION4 + 1000) is None)
assert(db.getLocations()[3] is location)
db.commit()

## Adding a fourth issue
db.addIssue(id = ID_ISSUE4, userId = USERNAME4, type = TYPE_NAME4, location = LOCATION_NAME4)
assert(len(db.getIssues()) == 4)
issue = db.getIssue(id = ID_ISSUE4)
assert(issue is not None)
assert(issue.id == ID_ISSUE4)
assert(issue.userId == USERNAME4)
assert(issue.type == TYPE_NAME4)
assert(issue.location == LOCATION_NAME4)
assert(db.getIssue(ID_ISSUE4 + 1000) is None)
assert(db.getIssues()[3] is issue)
db.commit()

print("################ DB TESTS DONE ###################")
# Provided API tests
print("################   API TESTS   ###################")

app.config['TESTING'] = True
client = app.test_client()
#testing the user_list funciton
r = client.get('/user')
assert(r.status_code == 200)
assert(len(r.json['users']) == 4)
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
#testing for the create_user_with_username function
r = client.put('/user/millerl19', json = {'password' : "pdislife", 'first' : "Lucas", 'last' : "Miller"})
assert(r.status_code == 201)
assert(r.json['ok'] == "user created")
r = client.get('/user')
assert(r.status_code == 200)
assert(len(r.json['users']) == 5)
assert("users" in r.json and "link" in r.json["users"][4] and "username" in r.json["users"][4] and "first" in r.json['users'][4] and "last" in r.json['users'][4])
assert(r.json['users'][4]['username'] == "millerl19")
assert(r.json['users'][4]['first'] == "Lucas")
assert(r.json['users'][4]['last'] == "Miller")
r = client.put('/user/davish20', json = {'password' : "pdislife", 'first' : "Lucas", 'last' : "Miller"})
assert(r.status_code == 403)
assert(r.json['error'] == "There is already a user using this username.")
r = client.put("user/hedrickj19", json ={'first' : "Lucas", 'last' : "Miller"})
assert(r.status_code == 403)
assert(r.json['error'] == 'must provide a password field')
r = client.put("user/hedrickj19", json ={'first' : "Lucas", 'last' : "Miller"})
assert(r.status_code == 403)
assert(r.json['error'] == 'must provide a password field')
r = client.put("user/hedrickj19", json ={'password' : "pdiflife", 'last' : "Miller"})
assert(r.status_code == 403)
assert(r.json['error'] == 'must provide a first field')
r = client.put("user/hedrickj19", json ={'first' : "Lucas", 'password' : "pdislife"})
assert(r.status_code == 403)
assert(r.json['error'] == 'must provide a last field')
#Test for the user_delete function
r = client.delete('/user/hedrickj19?password=pdislife')
assert(r.status_code == 404)
assert(r.json['error'] == "username not found in the database")
r = client.delete('/user/millerl19')
assert(r.status_code == 403)
assert(r.json['error'] == 'must provide a password parameter')
r = client.delete('user/millerl19?password=ballislife')
assert(r.status_code == 403)
assert(r.json['error'] == "Incorrect password.")
r = client.delete("/user/millerl19?password=pdislife")
assert(r.status_code == 204)
r  = client.get('/user/millerl19')
assert(r.status_code == 404)
assert(r.json['error'] == "username not found in the database")

#Test for the get_type function
r = client.get('/type')
assert(r.status_code == 200)
assert(len(r.json['types']) == 4)
assert('types' in r.json and "link" in r.json['types'][0] and 'id' in r.json['types'][0] and 'name' in r.json['types'][0])
assert(r.json['types'][0]["name"] == "Email")
assert(r.json['types'][0]["id"] == 1)

#Test for the find_type function
r = client.get('/type/1')
assert(r.status_code == 200)
assert(r.json['name'] == "Email")
assert(r.json['id'] == 1)
r = client.get('/type/988')
assert(r.status_code == 404)
assert(r.json['error'] == "typeId not found")
#Tests the for the create_type_with_id function
r = client.put('/type/5', json = {"name" : "Internet"})
assert(r.status_code == 201)
assert(r.json['ok'] == 'type created')
r = client.get('/type')
assert(r.status_code == 200)
assert(len(r.json['types']) == 5)
assert(r.json['types'][4]['name'] == "Internet")
r = client.put('/type/3', json = {'name' : "Phone"})
assert(r.status_code == 403)
assert(r.json['error'] == "There is already a type using this id.")
r = client.put('/type/6')
assert(r.status_code == 403)
assert(r.json['error'] == 'must provide a name field')
#Testing the delete_type function
r = client.delete('/type/88')
assert(r.status_code == 404)
assert(r.json['error'] == "typeId not found")
r = client.delete('/type/5')
assert(r.status_code == 204)
r = client.get('/type')
assert(r.status_code == 200)
assert(len(r.json['types']) == 4)
#Testing the create_type function
r = client.post('/type', json = {'name' : "Network"})
assert(r.status_code == 201)
assert(r.json['ok'] == 'type created')
r = client.get('/type')
assert(r.status_code == 200)
assert(len(r.json['types']) == 5)
assert(r.json['types'][4]['name'] == "Network")
r = client.post('/type')
assert(r.status_code == 403)
assert(r.json['error'] == "must provide a name field")
#Test for the get_location function
r = client.get('/location')
assert(r.status_code == 200)
assert(len(r.json['locations']) == 4)
assert('locations' in r.json and "link" in r.json['locations'][0] and 'id' in r.json['locations'][0] and 'name' in r.json['locations'][0])
assert(r.json['locations'][3]["name"] == "CFA")
assert(r.json['locations'][3]["id"] == 8)
#Test for the find_location function
r = client.get('/location/5')
assert(r.status_code == 200)
assert(r.json['name'] == "Science Center")
assert(r.json['id'] == 5)
r = client.get('/location/988')
assert(r.status_code == 404)
assert(r.json['error'] == "locationId not found")
#Tests the for the create_location_with_id function
r = client.put('/location/1', json = {"name" : "Crowe Hall"})
assert(r.status_code == 201)
assert(r.json['ok'] == 'location created')
r = client.get('/location')
assert(r.status_code == 200)
assert(len(r.json['locations']) == 5)
assert(r.json['locations'][4]['name'] == "Crowe Hall")
r = client.put('/location/8', json = {'name' : "Phone"})
assert(r.status_code == 403)
assert(r.json['error'] == "There is already a location using this id.")
r = client.put('/location/23')
assert(r.status_code == 403)
assert(r.json['error'] == 'must provide a name field')
#Testing the delete_location function
r = client.delete('/location/1')
assert(r.status_code == 404)
assert(r.json['error'] == "locationId not found")
r = client.delete('/location/5')
assert(r.status_code == 204)
r = client.get('/location')
assert(r.status_code == 200)
assert(len(r.json['locations']) == 4)
#Testing the create_location function
r = client.post('/location', json = {'name' : "Lambda"})
assert(r.status_code == 201)
assert(r.json['ok'] == 'location created')
r = client.get('/location')
assert(r.status_code == 200)
assert(len(r.json['locations']) == 5)
assert(r.json['locations'][4]['name'] == "Lambda")
r = client.post('/location')
assert(r.status_code == 403)
assert(r.json['error'] == "must provide a name field")
#Testing the get methods for the issue table paths
r = client.get('/issue')
assert(r.status_code == 200)
assert(len(r.json['issues']) == 4)
assert('issues' in r.json and 'id' in r.json['issues'][0] and 'type' in r.json['issues'][0] and 'description' in r.json['issues'][0] and 'location' in r.json['issues'][0])
assert(r.json['issues'][0]['id'] == 9)
assert(r.json['issues'][0]['type'] == "Email")
r = client.get('/issue/10')
assert(r.json['id'] == 10)
assert(r.json['type'] == "Phone")
assert(r.json['location'] == "Classic Hall")
assert(r.json['userId'] == "monnine20")
r = client.get('issue/34')
assert(r.status_code == 404)
assert(r.json['error'] == "issueId not found")
#Testing the create_issue_with_id function
r = client.put('/issue/21', json = {'username': "millerl19", 'type' : "Internet", 'description' : "Cannot connect to Internet", 'location' : "Crowe"})
assert(r.status_code == 201)
assert(r.json['ok'] == "issue created")
r  = client.get('/issue/21')
assert(r.status_code == 200)
assert(r.json['id'] == 21)
assert(r.json['userId'] == "millerl19")
assert(r.json['type'] == "Internet")
assert(r.json['description'] == "Cannot connect to Internet")
assert(r.json['location'] == "Crowe")
r = client.put('/issue/21')
assert(r.status_code == 403)
assert(r.json['error'] == "There is already a issue using this id.")
r = client.put('/issue/22', json = {'username' : "millerl19", 'type' : "Internet"})
assert(r.status_code == 201)
#Testing the create issue function
r = client.post('/issue', json = {"username" : "millerl19", "type" : "Internet", 'description':"Speeds are very slow", 'location' : "Crowe"})
assert(r.status_code == 201)
assert(r.json['ok'] == "issue created")
db.commit()
print("################ API TESTS DONE  #################")
