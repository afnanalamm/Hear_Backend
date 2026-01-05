# from sqlalchemy import DateTime, Date, Boolean, String, Integer, ForeignKey
from config import db
from datetime import datetime
from sqlalchemy.orm import relationship

class Address(db.Model):
    __tablename__ = 'addresses'
    addressID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    addressLine1 = db.Column(db.String(128), nullable=True)
    addressLine2 = db.Column(db.String(128), nullable=True)
    city = db.Column(db.String(64), nullable=True)
    state = db.Column(db.String(64), nullable=True)
    postCode = db.Column(db.String(32), nullable=True)

    # Back-reference to User (one-to-one-ish, assuming one address per user)
    user = relationship("User", back_populates="address", uselist=False)

    def to_json(self):
        return {
            "addressID": self.addressID,
            "addressLine1": self.addressLine1,
            "addressLine2": self.addressLine2,
            "city": self.city,
            "state": self.state,
            "postCode": self.postCode
        }


class User(db.Model):
    __tablename__ = 'users'

    userID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    addressID = db.Column(db.Integer, db.ForeignKey('addresses.addressID'), nullable=True)

    username = db.Column(db.String(64), nullable=True, unique=True, index=True)
    firstName = db.Column(db.String(64), nullable=True)
    lastName = db.Column(db.String(64), nullable=True)
    dateOfBirth = db.Column(db.String(64), nullable=True)

    contactNumber = db.Column(db.String(32), nullable=True)
    emailAddress = db.Column(db.String(64), nullable=True, unique=True, index=True)
    passwordHash = db.Column(db.String(512), nullable=True)

    superUser = db.Column(db.String(8), nullable=True)
    createdOn = db.Column(db.String(64), nullable=True)

    # Relationships
    address = relationship("Address", back_populates="user")

    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    reactions = relationship("Reaction", back_populates="user")

    # Notifications RECEIVED by this user
    notifications = relationship(
        "Notification",
        foreign_keys="Notification.userID",
        back_populates="user"
    )

    def to_json(self):
        return {
            "userID": self.userID,
            "addressID": self.addressID,
            "username": self.username,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "dateOfBirth": self.dateOfBirth,
            "contactNumber": self.contactNumber,
            "emailAddress": self.emailAddress,
            "passwordHash": self.passwordHash,
            "superUser": self.superUser,
            "createdOn": self.createdOn
        }

''
class Post(db.Model):
    __tablename__ = 'posts'
    postID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userID = db.Column(db.Integer, db.ForeignKey('users.userID'), nullable=True)

    interactionsID = db.Column(db.String(64))
    title = db.Column(db.String(320), nullable=True)
    uniqueTitle_for_media = db.Column(db.String(256), nullable=True)

    description = db.Column(db.String(12800), nullable=True)
    postType = db.Column(db.String(128), nullable=True)
    mediaAttached = db.Column(db.String(12), nullable=True)
    mediaType = db.Column(db.String(64), nullable=True)
    mediaURL = db.Column(db.String(128), nullable=True)

    deadline = db.Column(db.String(128), nullable=True)
    location = db.Column(db.String(128), nullable=True)
    tags = db.Column(db.String(1280), nullable=True)
    createdOn = db.Column(db.String(128), nullable=True)

    # Relationships
    user = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
    reactions = relationship("Reaction", back_populates="post")
    notifications = relationship("Notification", back_populates="post")

    def to_json(self):
        # Live agree/disagree counts from Reaction table
        agree_count = db.session.query(Reaction).filter_by(postID=self.postID, reactionType="agree").count()
        disagree_count = db.session.query(Reaction).filter_by(postID=self.postID, reactionType="disagree").count()

        return {
            "postID": self.postID,
            "userID": self.userID,
            "title": self.title,
            "uniqueTitle_for_media": self.uniqueTitle_for_media,
            "interactionsID": self.interactionsID,
            "description": self.description,
            "postType": self.postType,
            "mediaAttached": self.mediaAttached,
            "mediaType": self.mediaType,
            "mediaURL": self.mediaURL,
            "deadline": self.deadline,
            "location": self.location,
            "tags": self.tags,
            "createdOn": self.createdOn,
            "agreeCount": agree_count,
            "disagreeCount": disagree_count
        }


class Comment(db.Model):
    __tablename__ = 'comments'
    commentID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    postID = db.Column(db.Integer, db.ForeignKey('posts.postID'), nullable=True)
    userID = db.Column(db.Integer, db.ForeignKey('users.userID'), nullable=True)

    commentText = db.Column(db.String(1280), nullable=True)
    createdOn = db.Column(db.String(128), nullable=True)

    # Relationships
    post = relationship("Post", back_populates="comments")
    user = relationship("User", back_populates="comments")

    def to_json(self):
        return {
            "commentID": self.commentID,
            "postID": self.postID,
            "userID": self.userID,
            "commentText": self.commentText,
            "createdOn": self.createdOn
        }


class Reaction(db.Model):
    __tablename__ = 'reactions'
    reactionID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    postID = db.Column(db.Integer, db.ForeignKey('posts.postID'), nullable=False)
    userID = db.Column(db.Integer, db.ForeignKey('users.userID'), nullable=False)
    reactionType = db.Column(db.String(20), nullable=False)  # "agree" or "disagree"
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (db.UniqueConstraint('postID', 'userID', name='unique_user_post_reaction'),)

    # Relationships
    post = relationship("Post", back_populates="reactions")
    user = relationship("User", back_populates="reactions")

    def to_json(self):
        return {
            "reactionID": self.reactionID,
            "postID": self.postID,
            "userID": self.userID,
            "reactionType": self.reactionType,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None
        }


class Notification(db.Model):
    __tablename__ = 'notifications'

    notificationID = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # User who RECEIVES the notification
    userID = db.Column(db.Integer, db.ForeignKey('users.userID'), nullable=True)

    # User who TRIGGERED the notification
    fromUserID = db.Column(db.Integer, db.ForeignKey('users.userID'), nullable=True)

    postID = db.Column(db.Integer, db.ForeignKey('posts.postID'), nullable=True)
    commentID = db.Column(db.Integer, db.ForeignKey('comments.commentID'), nullable=True)

    notificationType = db.Column(db.String(64), nullable=True)
    isRead = db.Column(db.String(10), nullable=True)
    createdOn = db.Column(db.String(128), nullable=True)

    # Relationships
    user = relationship(
        "User",
        foreign_keys=[userID],
        back_populates="notifications"
    )

    from_user = relationship(
        "User",
        foreign_keys=[fromUserID]
    )

    post = relationship("Post", back_populates="notifications")
    comment = relationship("Comment")

    def to_json(self):
        return {
            "notificationID": self.notificationID,
            "userID": self.userID,
            "fromUserID": self.fromUserID,
            "postID": self.postID,
            "commentID": self.commentID,
            "notificationType": self.notificationType,
            "isRead": self.isRead,
            "createdOn": self.createdOn
        }

    __tablename__ = 'notifications'
    notificationID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userID = db.Column(db.Integer, db.ForeignKey('users.userID'), nullable=True)
    postID = db.Column(db.Integer, db.ForeignKey('posts.postID'), nullable=True)
    commentID = db.Column(db.Integer, db.ForeignKey('comments.commentID'), nullable=True)
    fromUserID = db.Column(db.Integer, db.ForeignKey('users.userID'), nullable=True)
    notificationType = db.Column(db.String(64), nullable=True)
    isRead = db.Column(db.String(10), nullable=True)
    createdOn = db.Column(db.String(128), nullable=True)

    # Relationships
    user = relationship("User", foreign_keys=[userID], back_populates="notifications")
    post = relationship("Post", back_populates="notifications")
    comment = relationship("Comment")
    from_user = relationship("User", foreign_keys=[fromUserID])

    def to_json(self):
        return {
            "notificationID": self.notificationID,
            "userID": self.userID,
            "postID": self.postID,
            "commentID": self.commentID,
            "fromUserID": self.fromUserID,
            "notificationType": self.notificationType,
            "isRead": self.isRead,
            "createdOn": self.createdOn
        }