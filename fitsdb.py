# Sets up database
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from json import dumps

Base = declarative_base()

class User(Base):
   __tablename__ = 'users'
   
   username = Column(String, nullable = False, primary_key = True, unique = True)
   first = Column(String, nullable = False)
   last = Column(String, nullable = False)
   password = Column(String, nullable = False)

   issues = relationship("Issue", back_populates="user")
   # def __repr__(self):
   #    if self.description is not None:
   #       bucket_str = "Bucket ID: " + self.id + "\nDescription: " + self.description + "\nPassword Hash: " + self.passwordHash + '\n'
   #    else:
   #       bucket_str = "Bucket ID: " + self.id + "\nDescription: " + "None" + "\nPassword Hash: " + self.passwordHash + '\n'
   #    return bucket_str


class Issue(Base):
   __tablename__ = 'issues'
   
   id = Column(String, nullable = False, primary_key = True)
   userId = Column(String, ForeignKey(User.username, ondelete = "CASCADE"), nullable = False)
   type = Column(String, ForeignKey("types.name", ondelete = "CASCADE"), nullable = False)
   description = Column(String, nullable = True)
   location = Column(String, ForeignKey("locations.name", ondelete = "CASCADE"), nullable = True)

   user = relationship("User", back_populates="issues")

   # def __repr__(self):
   #    shortcut_str = "Link Hash: " + self.linkHash + "\nBucker ID: " + self.bucketId + "\nLink: "\
   #     + self.link + "\nDescription: " + self.description + '\n'
   #    return shortcut_str

class Type(Base):
   __tablename__ = 'types'

   id = Column(Integer, nullable = False, primary_key = True)
   name = Column(String, nullable = False, unique = True)

class Location(Base):
   __tablename__ = 'locations'

   id = Column(Integer, nullable = False, primary_key = True)
   name = Column(String, nullable = False, unique = True)



# Represents the database and our interaction with it
class Db:
   def __init__(self):
      engineName = 'sqlite:///test.db'   # Uses in-memory database
      self.engine = create_engine(engineName)
      self.metadata = Base.metadata
      self.metadata.bind = self.engine
      self.metadata.drop_all(bind=self.engine)
      self.metadata.create_all(bind=self.engine)
      Session = sessionmaker(bind=self.engine)
      self.session = Session()

   def commit(self):
      self.session.commit()

   def rollback(self):
      self.session.rollback()

   # TODO Must implement the following methods
   def getUsers(self):
      return self.session.query(User).all()

   def getUser(self, username):
      return self.session.query(User)\
                 .filter_by(username = username)\
                 .one_or_none()

   def addUser(self, username, first, last, password):
      user = User(username = username, first = first, last = last, password = password)
      self.session.add(user)
      return user

   def deleteUser(self, user):
      self.session.delete(user)
