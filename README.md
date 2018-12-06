fits - An Online API used to track IT issues in a school or business

FITS will use an SQLLite database to store all information with 4 Primary Tables:
  1. Users
  2. Issues
  3. Types
  4. Locations

API Paths and Methods:
  * /user
    -GET: Returns a list of all user currently in the system
    
  * /user/'<username>'
    -GET: Returns the user information and issues entered by the user with the given username (Password must be given in the query)
    -PUT: Creates a new user with the given username (first, last, and password information must also be passed in json of the request)
    -DELETE: Deletes the user with the given username (Password must be given in the query)
  
  * /type
    -GET: Returns a list of all types currently in the system
    -POST: Creates a type object with a random id (name information must be passed in the json of the request)
  
  * /type/'<id>'
    -GET: Returns the type information and issues entered under that type with the given id
    -PUT: Creates a type object with the given id (name information must be passed in the json of the request)
    -DELETE: Deletes the type object with the given id
  
  * /location
    -GET: Returns a list of all locations currently in the system
    -POST: Creates a location object with a random id (name information must be passed in the json of the request)
  
  * /location/<id>
    -GET: Returns the location information and issues entered under that location with the given id
    -PUT: Creates a location object with the given id (name information must be passed in the json of the request)
    -DELETE: Deletes the location object with the given id
  
  * /issue
    -GET: Returns a list of all the issues currently in the system
    -POST: Creates an issue with a random id (username and type information must be passed in the json of the request, description and                location optional)
  
  * /issue/<id>
    -GET: Returns the issue with the given id and all of its information
    -PUT: Creates an issue with the given id (username and type information must be passed in the json of the request, description and                location optional)
    -DELETE: Deletes the issue with the given id
  
  * /issue/user/<username>
    -GET: Returns all the issues added by the user with the given username
  
  * /issue/type/<name>
    -GET: Returns all the issues under the type with the given name
  
  * /issue/location/<name>
    -GET: Returns all the issues under the location with the given name
