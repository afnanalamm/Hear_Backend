# from sqlalchemy import DateTime, Date, Boolean, String, Integer, ForeignKey
from config import db
from datetime import datetime  # This was missing!

class Address(db.Model):
   __tablename__ = 'addresses'
   addressID = db.Column(db.Integer, primary_key = True, autoincrement=True)
   addressLine1 = db.Column(db.String(128), nullable = True)
   addressLine2 = db.Column(db.String(128), nullable = True)
   city = db.Column(db.String(64), nullable = True)
   state = db.Column(db.String(64), nullable = True)
   postCode = db.Column(db.String(32), nullable = True)

   def to_json(self):
       return {
           "addressID" : self.addressID,
           "addressLine1" : self.addressLine1,
           "addressLine2" : self.addressLine2,
           "city": self.city,
           "state" : self.state,
           "postCode" : self.postCode
       }

class Comment(db.Model):
   __tablename__ = 'comments'
   commentID = db.Column(db.Integer, primary_key = True, autoincrement=True)
   postID = db.Column(db.String(64),  nullable = True)
   userID = db.Column(db.String(64),  nullable = True)

   commentText = db.Column(db.String(1280), nullable = True)
   createdOn = db.Column(db.String(128), nullable = True)

   def to_json(self):
       return {
           "commentID" : self.commentID,
           "postID" : self.postID,
           "userID" : self.userID,
           "commentText": self.commentText,
           "createdOn" : self.createdOn
       }

class Notification(db.Model):
   __tablename__ = 'notifications'
   notificationID = db.Column(db.Integer, primary_key = True, autoincrement=True)
   userID = db.Column(db.String(64),  nullable = True)
   postID = db.Column(db.String(64),  nullable = True)
   commentID = db.Column(db.String(64),  nullable = True)
   fromUserID = db.Column(db.String(64),  nullable = True)
   notificationType = db.Column(db.String(64),  nullable = True)
   isRead = db.Column(db.String(10), nullable = True)
   createdOn = db.Column(db.String(128), nullable = True)

   def to_json(self):
       return {
           "notificationID" : self.notificationID,
           "userID" : self.userID,
           "postID" : self.postID,
           "commentID": self.commentID,
           "fromUserID" : self.fromUserID,
           "notificationType" : self.notificationType,
           "isRead" : self.isRead,
           "createdOn" : self.createdOn
       }

class Reaction(db.Model):
   __tablename__ = 'reactions'
   reactionID = db.Column(db.Integer, primary_key=True, autoincrement=True)
   postID = db.Column(db.Integer, db.ForeignKey('posts.postID'), nullable=False)
   userID = db.Column(db.String(64), nullable=False)
   reactionType = db.Column(db.String(20), nullable=False)  # "agree" or "disagree"
   timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

   __table_args__ = (db.UniqueConstraint('postID', 'userID', name='unique_user_post_reaction'),)

   def to_json(self):
       return {
           "reactionID": self.reactionID,
           "postID": self.postID,
           "userID": self.userID,
           "reactionType": self.reactionType,
           "timestamp": self.timestamp.isoformat() if self.timestamp else None
       }

class Post(db.Model):
   __tablename__ = 'posts'
   postID = db.Column(db.Integer, primary_key = True, autoincrement=True)
   userID = db.Column(db.String(64), nullable = True)

   interactionsID = db.Column(db.String(64))
   title = db.Column(db.String(320), nullable = True)
   uniqueTitle_for_media = db.Column(db.String(256), nullable = True)

   description = db.Column(db.String(12800), nullable = True)
   postType = db.Column(db.String(128), nullable = True)
   mediaAttached = db.Column(db.String(12), nullable = True)
   mediaType = db.Column(db.String(64), nullable = True)
   mediaURL = db.Column(db.String(128), nullable = True)

   deadline = db.Column(db.String(128), nullable = True)
   location = db.Column(db.String(128), nullable = True)
   tags = db.Column(db.String(1280), nullable = True)
   createdOn = db.Column(db.String(128), nullable = True)

   # THIS WAS OUTSIDE THE CLASS BEFORE → NOW FIXED
   def to_json(self):
       # Live agree/disagree counts from Reaction table
       agree_count = db.session.query(Reaction).filter_by(postID=self.postID, reactionType="agree").count()
       disagree_count = db.session.query(Reaction).filter_by(postID=self.postID, reactionType="disagree").count()

       return {
           "postID" : self.postID,
           "userID" : self.userID,
           "title": self.title,
           "uniqueTitle_for_media": self.uniqueTitle_for_media,
           "interactionsID" : self.interactionsID,
           "description": self.description,
           "postType" : self.postType,
           "mediaAttached" : self.mediaAttached,
           "mediaType" : self.mediaType,
           "mediaURL" : self.mediaURL,
           "deadline": self.deadline,
           "location" : self.location,
           "tags" : self.tags,
           "createdOn" : self.createdOn,
           "agreeCount": agree_count,        # Real count
           "disagreeCount": disagree_count   # Real count
       }



class User(db.Model):
   __tablename__ = 'users'
   userID = db.Column(db.Integer, primary_key = True, autoincrement=True)
   addressID = db.Column(db.String(64), nullable = True)

   username = db.Column(db.String(64),  nullable = True, unique=True, index= True)
   firstName = db.Column(db.String(64),  nullable = True)
   lastName = db.Column(db.String(64),  nullable = True)
   dateOfBirth = db.Column(db.String(64), nullable = True)

   contactNumber = db.Column(db.String(32), nullable = True)
   emailAddress = db.Column(db.String(64), nullable = True, unique=True, index=True)
   passwordHash = db.Column(db.String(512), nullable = True)

   superUser = db.Column(db.String(10), nullable = True)
   createdOn = db.Column(db.String(64), nullable = True)

   def to_json(self):
       return {
           "userID" : self.userID,
           # "addressID" : self.addressID,
           "username": self.username,
           "firstName" : self.firstName,
           "lastName" : self.lastName,
           "dateOfBirth" : self.dateOfBirth,
           "contactNumber": self.contactNumber,
           "emailAddress" : self.emailAddress,
           "passwordHash" : self.passwordHash,
           "superUser": self.superUser,
           "createdOn" : self.createdOn
       }