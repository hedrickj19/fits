from flask import Flask, request, make_response, json, url_for, abort
from fitsdb import Db   # See db.py
from utils import makeId, getHash

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

@app.route('/issue/<id>', methods = ['GET'])
def find_issue(id):
   return True





#Helper functions
def findUser(username):
   user = db.getUser(username)
   if user is None:
      abort(404, "username not found in the database")
   return user

##Helper functions used for user verification
def getPasswordFromQuery():
   if "password" not in request.args:
      abort(403, 'must provide a password parameter')
   return request.args["password"]

#Helper function that checks if a given password is correct
def checkPassword(user, password):
   hash = getHash(password)
   if hash != user.password:
      abort(403, "Incorrect password.")

# Starts the application
if __name__ == "__main__":
   app.run()
