# from sqlalchemy import DateTime, Date, Boolean, String, Integer, ForeignKey
from config import db

class Address(db.Model):
    __tablename__ = 'addresses'
    addressID = db.Column(db.Integer, primary_key = True, autoincrement=True)
    addressLine1 = db.Column(db.String(100), nullable = False)
    addressLine2 = db.Column(db.String(100), nullable = True)
    city = db.Column(db.String(50), nullable = False)
    state = db.Column(db.String(50), nullable = False)
    postCode = db.Column(db.String(20), nullable = False)
    
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
    postID = db.Column(db.String(80),  nullable = False)
    userID = db.Column(db.String(80),  nullable = False)

    commentText = db.Column(db.String(1000), nullable = False)
    createdOn = db.Column(db.String(100), nullable = False)

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
    postID = db.Column(db.String(80),  nullable = False)

    numAgree = db.Column(db.String(10), nullable = False)
    numDisagree = db.Column(db.String(10), nullable = False)
    comments = db.Column(db.String(10), nullable = False)
    approved = db.Column(db.String(10), nullable = False)

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
    userID = db.Column(db.String(80),  nullable = False)
    postID = db.Column(db.String(80),  nullable = False)
    commentID = db.Column(db.String(80),  nullable = False)
    fromUserID = db.Column(db.String(80),  nullable = False)
    notificationType = db.Column(db.String(80),  nullable = False)
    isRead = db.Column(db.String(10), nullable = False)
    createdOn = db.Column(db.String(100), nullable = False)

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
    userID = db.Column(db.String(80),  nullable = False)

    interactionsID = db.Column(db.String(80))


    description = db.Column(db.String(10000), nullable = False)
    postType = db.Column(db.String(100), nullable = False)
    mediaAttached = db.Column(db.String(12), nullable = True)
    mediaType = db.Column(db.String(80), nullable = True)
    mediaURL = db.Column(db.String(100), nullable = True)

    deadline = db.Column(db.String(100), nullable = True)
    location = db.Column(db.String(100), nullable = False)
    tags = db.Column(db.String(1000), nullable = True)
    createdOn = db.Column(db.String(100), nullable = False)


    def to_json(self):
        return {
            "postID" : self.postID,
            "userID" : self.userID,
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

    username = db.Column(db.String(80),  nullable = False, unique=True, index= True)
    firstName = db.Column(db.String(80),  nullable = False)
    lastName = db.Column(db.String(80),  nullable = False)
    dateOfBirth = db.Column(db.String(80), nullable = False)

    contactNumber = db.Column(db.String(20), nullable = False)
    emailAddress = db.Column(db.String(80), nullable = False, unique=True, index=True)
    passwordHash = db.Column(db.String(300), nullable = False)

    superUser = db.Column(db.String(10), nullable = True)
    createdOn = db.Column(db.String(80), nullable = False)

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





















































# from config import db

# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key = True, autoincrement=True)
#     username = db.Column(db.String(80),  nullable = False)
#     description = db.Column(db.String(80),  nullable = False)
#     postType = db.Column(db.String(10), nullable = False)
#     mediaFilepath = db.Column(db.String(1000), nullable = True)
#     date = db.Column(db.String(120), nullable = False)
#     location = db.Column(db.String(80), nullable = False)
#     tags = db.Column(db.String(100), nullable = True)

#     def to_json(self):
#         return {
#             "id" : self.id,
#             "username" : self.username,
#             "description" : self.description,
#             "postType": self.postType,
#             "mediaFilepath" : self.mediaFilepath,
#             "date" : self.date,
#             "location" : self.location,
#             "tags" : self.tags
#         }


