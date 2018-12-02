from flask import Flask, request, make_response, json, url_for, abort
from fitsdb import Db   # See db.py
from utils import makeId, getHash
import random

app = Flask(__name__)
db = Db()
app.debug = True # Comment out when not testing
app.url_map.strict_slashes = False   # Allows for a trailing slash on routes

#### ERROR HANDLERS

@app.errorhandler(500)
def server_error(e):
   return make_json_response({ 'error': 'unexpected server error' }, 500)

@app.errorhandler(404)
def not_found(e):
   return make_json_response({ 'error': e.description }, 404)

@app.errorhandler(403)
def forbidden(e):
   return make_json_response({ 'error': e.description }, 403)

@app.errorhandler(400)
def client_error(e):
   return make_json_response({ 'error': e.description }, 400)

## Helper method for creating JSON responses
def make_json_response(content, response = 200, headers = {}):
   headers['Content-Type'] = 'application/json'
   return make_response(json.dumps(content), response, headers)

#### MAIN ROUTES

#### User Table Paths
@app.route('/user', methods = ['GET'])
def user_list():
   users = db.getUsers()
   return make_json_response({
      "users": [
         {
            "link": url_for('find_user', username = user.username) ,
            "username" : user.username,
            "first" : user.first,
            "last" : user.last}
         for user in users
      ]
   })

@app.route('/user/<username>', methods = ['GET'])
def find_user(username):
   user = findUser(username)
   password = getPasswordFromQuery()
   checkPassword(user, password)
   return make_json_response({
      "username" : user.username,
      "link" : url_for('find_user', username = user.username),
      "first" : user.first,
      "last" : user.last,
      "issues" : [
      {
         "id" : issue.id,
         "link" : url_for('find_issue', id = issue.id),
         "description" : issue.description,
         "location" : issue.location}
         for issue in user.issues]
      })

@app.route('/user/<username>', methods = ['PUT'])
def create_user_with_username(username):
   user = checkUserExsists(username)
   password = getPasswordFromContents()
   first_name = getFirstFromContents()
   last_name = getLastFromContents()
   db.addUser(username, first_name, last_name, getHash(password))
   headers = {"Location" : url_for('find_user', username = username)}
   return make_json_response({ 'ok': 'user created' }, 201, headers)

@app.route('/user/<username>', methods = ['DELETE'])
def user_delete(username):
   user = findUser(username)
   password = getPasswordFromQuery()
   checkPassword(user, password)
   db.deleteUser(user)
   db.commit()
   return make_json_response({'ok' : 'user deleted'}, 204)

#### Type Table Paths
@app.route('/type', methods = ['GET'])
def type_list():
   types = db.getTypes()
   return make_json_response({
      "types": [
         {
            "link": url_for('find_type', id = type.id) ,
            "id" : type.id,
            "name" : type.name}
         for type in types
      ]
   })

@app.route('/type/<id>', methods = ['GET'])
def find_type(id):
   type = findType(id)
   return make_json_response({
      "id" : type.id,
      "link" : url_for('find_type', id = type.id),
      "name" : type.name,
      "issues" : [
      {
         "id" : issue.id,
         "link" : url_for('find_issue', id = issue.id),
         "description" : issue.description,
         "location" : issue.location}
         for issue in type.issues]
      })

@app.route('/type/<id>', methods = ['PUT'])
def create_type_with_id(id):
   type = checkTypeExsists(id)
   name = getNameFromContents()
   db.addType(type, name)
   headers = {"Location" : url_for('find_type', id = id)}
   return make_json_response({ 'ok': 'type created' }, 201, headers)

@app.route('/type', methods = ['POST'])
def create_type():
   id = generateID("type")
   return create_type_with_id(id)

@app.route('/type/<id>', methods = ['DELETE'])
def type_delete(id):
   type = findType(id)
   db.deleteType(type)
   db.commit()
   return make_json_response({'ok' : 'type deleted'}, 204)

#### Location Table Paths
@app.route('/location', methods = ['GET'])
def location_list():
   locations = db.getLocations()
   return make_json_response({
      "locations": [
         {
            "link": url_for('find_location', id = location.id) ,
            "id" : location.id,
            "name" : location.name}
         for location in locations
      ]
   })

@app.route('/location/<id>', methods = ['GET'])
def find_location(id):
   location = findLocation(id)
   return make_json_response({
      "id" : location.id,
      "link" : url_for('find_location', id = location.id),
      "name" : location.name,
      "issues" : [
      {
         "id" : issue.id,
         "link" : url_for('find_issue', id = issue.id),
         "description" : issue.description,
         "location" : issue.location}
         for issue in location.issues]
      })

@app.route('/location/<id>', methods = ['PUT'])
def create_location_with_id(id):
   location = checkLocationExsists(id)
   name = getNameFromContents()
   db.addLocation(location, name)
   headers = {"Location" : url_for('find_location', id = id)}
   return make_json_response({ 'ok': 'location created' }, 201, headers)



@app.route('/issue/<id>', methods = ['GET'])
def find_issue(id):
   return True





#Helper functions
def findUser(username):
   user = db.getUser(username)
   if user is None:
      abort(404, "username not found in the database")
   return user

def findType(id):
   type = db.getType(id)
   if type is None:
      abort(404, "typeId not found")
   return type

def findLocation(id):
   location = db.getLocation(id)
   if location is None:
      abort(404, "locationId not found")
   return location

#Helper funciton used to see if a user already exsist when trying to make a new user
def checkUserExsists(username):
   user = db.getUser(username)
   if user is not None:
      abort(403, "There is already a user using this username.")
   return user

def checkTypeExsists(id):
   type = db.getType(id)
   if type is not None:
      abort(403, "There is already a type using this id.")
   return type

def checkLocationExsists(id):
   location = db.getLocation(id)
   if location is not None:
      abort(403, "There is already a location using this id.")
   return location



##Helper functions used for user verification
def getPasswordFromQuery():
   if "password" not in request.args:
      abort(403, 'must provide a password parameter')
   return request.args["password"]

#Helper functions to get information from the json object passed through the request
def getPasswordFromContents():
   contents = request.get_json()
   if contents is None or "password" not in contents:
      abort(403, 'must provide a password field')
   return contents["password"]

def getFirstFromContents():
   contents = request.get_json()
   if "first" not in contents:
      abort(403, 'must provide a first field')
   return contents['first']

def getLastFromContents():
   contents = request.get_json()
   if "last" not in contents:
      abort(403, 'must provide a last field')
   return contents['last']

def getNameFromContents():
   contents = request.get_json()
   if contents is None or "name" not in contents:
      abort(403, 'must provide a name field')
   return contents['name']

#Helper function that checks if a given password is correct
def checkPassword(user, password):
   hash = getHash(password)
   if hash != user.password:
      abort(403, "Incorrect password.")

#Helper Function to Generate a random id
def generateID(table):
   id = random.randint(1,10000)
   if table == "type":
      while db.getType(id) is not None:
         id = random.randint(1,10000)
   if table == "location":
      while db.getLocation(id) is not None:
         id = random.randint(1,10000)
   return id

# Starts the application
if __name__ == "__main__":
   app.run()
