from config import db

class Post(db.Model):
    postID = db.Column(db.Integer, primary_key = True)

    userID = db.Column(db.String(80),  nullable = False)
    interactionsID = db.Column(db.String(80),  nullable = False)
    description = db.Column(db.String(10000), nullable = False)
    postType = db.Column(db.String(10), nullable = False)
    location = db.Column(db.String(100), nullable = False)
    createdOn = db.Column(db.String(100), nullable = False)

    mediaAttached = db.Column(db.String(12), nullable = True)
    mediaType = db.Column(db.String(80), nullable = True)
    mediaURL = db.Column(db.String(100), nullable = True)
    deadline = db.Column(db.String(100), nullable = True)
    tags = db.Column(db.String(1000), nullable = True)

    def to_json(self):
        return {
            "postID" : self.postID,
            "userID" : self.userID,
            "interactionsID" : self.interactionsID,
            "description": self.description,
            "postType" : self.postID,
            "mediaAttached" : self.mediaAttached,
            "mediaType" : self.mediaType,
            "mediaURL" : self.mediaURL,
            "location" : self.location,
            "createdOn" : self.createdOn,
            "deadline": self.deadline,
            "tags" : self.tags
        }















# from config import db

# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
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


