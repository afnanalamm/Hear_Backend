# from sqlalchemy import DateTime, Date, Boolean, String, Integer, ForeignKey
from config import db

class Address(db.Model):
    __tablename__ = 'addresses'
    addressID = db.Column(db.Integer, primary_key = True, autoincrement=True)
    addressLine1 = db.Column(db.String(100), nullable = True)
    addressLine2 = db.Column(db.String(100), nullable = True)
    city = db.Column(db.String(50), nullable = True)
    state = db.Column(db.String(50), nullable = True)
    postCode = db.Column(db.String(20), nullable = True)
    
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
    postID = db.Column(db.String(80),  nullable = True)
    userID = db.Column(db.String(80),  nullable = True)

    commentText = db.Column(db.String(1000), nullable = True)
    createdOn = db.Column(db.String(100), nullable = True)

    def to_json(self):
        return {
            "commentID" : self.commentID,
            "postID" : self.postID,
            "userID" : self.userID,
            "commentText": self.commentText,
            "createdOn" : self.createdOn
        }

class Interaction(db.Model):
    __tablename__ = 'interactions'
    interactionsID = db.Column(db.Integer, primary_key = True, autoincrement=True)
    postID = db.Column(db.String(80),  nullable = True)

    numAgree = db.Column(db.String(10), nullable = True)
    numDisagree = db.Column(db.String(10), nullable = True)
    comments = db.Column(db.String(10), nullable = True)
    approved = db.Column(db.String(10), nullable = True)

    def to_json(self):
        return {
            "interactionsID" : self.interactionsID,
            "postID" : self.postID,
            "numAgree": self.numAgree,
            "numDisagree" : self.numDisagree,
            "comments" : self.comments,
            "approved" : self.approved
        }

class Notification(db.Model):
    __tablename__ = 'notifications'
    notificationID = db.Column(db.Integer, primary_key = True, autoincrement=True)
    userID = db.Column(db.String(80),  nullable = True)
    postID = db.Column(db.String(80),  nullable = True)
    commentID = db.Column(db.String(80),  nullable = True)
    fromUserID = db.Column(db.String(80),  nullable = True)
    notificationType = db.Column(db.String(80),  nullable = True)
    isRead = db.Column(db.String(10), nullable = True)
    createdOn = db.Column(db.String(100), nullable = True)

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

class Post(db.Model):
    __tablename__ = 'posts'
    postID = db.Column(db.Integer, primary_key = True, autoincrement=True)
    userID = db.Column(db.String(80),  nullable = True)

    interactionsID = db.Column(db.String(80))
    title = db.Column(db.String(200), nullable = True)

    description = db.Column(db.String(10000), nullable = True)
    postType = db.Column(db.String(100), nullable = True)
    mediaAttached = db.Column(db.String(12), nullable = True)
    mediaType = db.Column(db.String(80), nullable = True)
    mediaURL = db.Column(db.String(100), nullable = True)

    deadline = db.Column(db.String(100), nullable = True)
    location = db.Column(db.String(100), nullable = True)
    tags = db.Column(db.String(1000), nullable = True)
    createdOn = db.Column(db.String(100), nullable = True)


    def to_json(self):
        return {
            "postID" : self.postID,
            "userID" : self.userID,
            "title": self.title,
            "interactionsID" : self.interactionsID,
            "description": self.description,
            "postType" : self.postType,
            "mediaAttached" : self.mediaAttached,
            "mediaType" : self.mediaType,
            "mediaURL" : self.mediaURL,
            "deadline": self.deadline,
            "location" : self.location,
            "tags" : self.tags,
            "createdOn" : self.createdOn
        }
    


class User(db.Model):
    __tablename__ = 'users'
    userID = db.Column(db.Integer, primary_key = True, autoincrement=True)
    addressID = db.Column(db.String(80), nullable = True)

    username = db.Column(db.String(80),  nullable = True, unique=True, index= True)
    firstName = db.Column(db.String(80),  nullable = True)
    lastName = db.Column(db.String(80),  nullable = True)
    dateOfBirth = db.Column(db.String(80), nullable = True)

    contactNumber = db.Column(db.String(20), nullable = True)
    emailAddress = db.Column(db.String(80), nullable = True, unique=True, index=True)
    passwordHash = db.Column(db.String(300), nullable = True)

    superUser = db.Column(db.String(10), nullable = True)
    createdOn = db.Column(db.String(80), nullable = True)

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
