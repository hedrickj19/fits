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


#### MAIN ROUTES

@app.route('/', methods = ['GET'])
def bucket_list():
   buckets = db.getBuckets()
   return make_json_response({
      "buckets": [
         {
            "link": url_for('bucket_contents', bucketId = bucket.id) ,
            "description" : bucket.description }
         for bucket in buckets
      ]
   })

@app.route('/<bucketId>', methods = ['GET'])
def bucket_contents(bucketId):
   bucket = findBucket(bucketId)
   password = getPasswordFromQuery()
   checkPassword(bucket, password)
   return make_json_response({
      "id" : bucket.id,
      "link" : url_for('bucket_contents', bucketId = bucket.id),
      "description" : bucket.description,
      "shortcuts" : [
      {
         "linkHash" : shortcut.linkHash,
         "link" : url_for('shortcut_get_link', bucketId = bucket.id, hash = shortcut.linkHash),
         "description" : shortcut.description}
         for shortcut in bucket.shortcuts]
      })

@app.route('/', methods = ['POST'])
def bucket_create():
   bucketId = generateId()
   return bucket_create_with_hash(bucketId)

@app.route('/<bucketId>', methods = ['PUT'])
def bucket_create_with_hash(bucketId):
   bucket = checkBucketExsists(bucketId)
   password = getPasswordFromContents()
   description = getDescriptionFromContents()
   db.addBucket(bucketId, getHash(password), description)
   headers = {"Location" : url_for('bucket_contents', bucketId = bucketId)}
   return make_json_response({ 'ok': 'bucket created' }, 201, headers)

@app.route('/<bucketId>', methods = ['DELETE'])
def bucket_delete(bucketId):
   bucket = findBucket(bucketId)
   password = getPasswordFromQuery()
   checkPassword(bucket, password)
   db.deleteBucket(bucket)
   db.commit()
   return make_json_response({'ok' : 'bucket deleted'}, 204)

@app.route('/<bucketId>/<hash>', methods = ['GET'])
def shortcut_get_link(bucketId, hash):
   bucket = findBucket(bucketId)
   shortcut = findShortcut(hash, bucket)
   headers = {"Location" : shortcut.link}
   return make_json_response({
      "hash" : hash,
      "link" : shortcut.link,
      "description" : shortcut.description
      }, 307, headers)


@app.route('/<bucketId>/<hash>', methods = ['PUT'])
def shortcut_create_with_hash(bucketId, hash):
   bucket= findBucket(bucketId)
   shortcut = db.getShortcut(hash, bucket)
   if shortcut is not None:
      abort(403, "hash is already in use")
   password = getPasswordFromContents()
   link = getLinkFromContents()
   checkPassword(bucket, password)
   description = getDescriptionFromContents()
   db.addShortcut(hash, bucket, link, description)
   db.commit()
   headers = {"Location" : url_for('shortcut_get_link', bucketId = bucketId, hash = hash)}
   return make_json_response({'ok' : "shortcut created"}, 201, headers)

@app.route('/<bucketId>', methods = ['POST'])
def shortcut_create(bucketId):
   bucket = findBucket(bucketId)
   new_hash = generateHash(bucket)
   return shortcut_create_with_hash(bucketId, new_hash)

@app.route('/<bucketId>/<hash>', methods = ['DELETE'])
def shortcut_delete(bucketId, hash):
   bucket = findBucket(bucketId)
   shortcut = findShortcut(hash, bucket)
   password = getPasswordFromQuery()
   checkPassword(bucket, password)
   db.deleteShortcut(shortcut)
   db.commit()
   return make_json_response({'ok' : "shortcut deleted"}, 204)



## Helper method for creating JSON responses
def make_json_response(content, response = 200, headers = {}):
   headers['Content-Type'] = 'application/json'
   return make_response(json.dumps(content), response, headers)

##Helper functions used for user verification
def getPasswordFromQuery():
   if "password" not in request.args:
      abort(403, 'must provide a password parameter')
   return request.args["password"]

def getPasswordFromContents():
   contents = request.get_json()
   if contents is None or "password" not in contents:
      abort(403, 'must provide a password field')
   return contents["password"]

def getDescriptionFromContents():
   contents = request.get_json()
   if "description" in contents:
      return contents['description']
   return None

def getLinkFromContents():
   contents = request.get_json()
   if "link" not in contents:
      abort(403, "Link required")
   return contents['link']

def findBucket(bucketId):
   bucket = db.getBucket(bucketId)
   if bucket is None:
      abort(404, "BucketId not found in the database")
   return bucket

def findShortcut(hash, bucket):
   shortcut = db.getShortcut(hash, bucket)
   if shortcut is None:
      abort(404, "No shortcut found")
   return shortcut

def checkBucketExsists(bucketId):
   bucket = db.getBucket(bucketId)
   if bucket is not None:
      abort(403, "There is already a bucket using this id.")
   return bucket

def checkPassword(bucket, password):
   hash = getHash(password)
   if hash != bucket.passwordHash:
      abort(403, "Incorrect password.")

def generateId():
   bucket = "test"
   while bucket is not None:
      id = makeId()
      bucket = db.getBucket(id)
   return id

def generateHash(bucket):
   new_hash = "test"
   while new_hash is not None:
      hash = makeId()
      new_hash = db.getShortcut(hash, bucket)
   return hash



# Starts the application
if __name__ == "__main__":
   app.run()
