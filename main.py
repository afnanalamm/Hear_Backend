from flask import request, jsonify
from config import app, db
from models import *
from sqlalchemy import *

@app.route("/check_login", methods=["POST"])
def check_login():
    try:
        login_data = request.json
        requestPasswordHash = login_data["passwordHash"]
        requestEmailAddress = login_data["emailAddress"]
        realPasswordHash = select(User).where(User.emailAddress == requestEmailAddress).first().passwordHash
        if (requestPasswordHash == realPasswordHash) and (requestEmailAddress == (select(User).where(User.emailAddress == requestEmailAddress).first().emailAddress)):
            return 200

        else:
            return jsonify({"Message": "Incorrect Attempt"}), 400

    except Exception as e:
        return jsonify({"Message": "Incorrect Attempt"}), 400
        
    



@app.route("/allposts", methods= ["GET"])
def get_posts():
    allposts = Post.query.all()

    json_allposts = (list(map(lambda x: x.to_json(), allposts)))
    lastToFirst_allposts = json_allposts[::-1]

    return jsonify(lastToFirst_allposts), 200


@app.route("/create_post", methods=["POST"])
def create_post():
    data = request.json
    required_fields = ["userID", "description", "postType", "deadline", "location"]
    
    # Check for required fields
    if not all(data.get(field) for field in required_fields):
        return jsonify({"message": "Missing required fields: Description, deadline, location"}), 400

    # Prepare post data
    post_data = {
        "userID": data["userID"],
        "description": data["description"],
        "postType": data["postType"],
        "deadline": data["deadline"],
        "location": data["location"],
        "mediaURL": data["mediaURL"],
        "tags": data["tags"],
        "createdOn": data["createdOn"]
    }

    # Create new post
    new_post = Post(**{k: v for k, v in post_data.items()}) # Only include non-None values. This avoids multiple conditionals. This uses dictionary unpacking.
    print("New post to be added:", new_post.to_json())      

    try:
        db.session.add(new_post)
        
        db.session.commit()
        print("New post added:", new_post)
    except Exception as e:
        return jsonify({"message": str(e)}), 400
        
    
    return jsonify({"message": "Post added!"}), 201


@app.route("/create_account", methods=["POST"])
def create_account():
    data = request.json
    required_fields = ["firstName", "lastName", "dateOfBirth", "contactNumber", "emailAddress", "username"]
    
    # Check for required fields
    # if not all(data.get(field) for field in required_fields):
    #     return jsonify({"message": "Missing required fields: Description, deadline, location"}), 400

    # create new account
    account_data = {
        
        "username": data["username"],
        "firstName": data["firstName"],
        "lastName": data["lastName"],
        "dateOfBirth": data["dateOfBirth"],
        "contactNumber": data["contactNumber"],
        "emailAddress": data["emailAddress"],
        "passwordHash": data["passwordHash"],
        "superUser": data["superUser"],
        "createdOn": data["createdOn"]
    }

    # Create new post
    new_account = User(**{k: v for k, v in account_data.items()}) # Only include non-None values. This avoids multiple conditionals. This uses dictionary unpacking.

  
    try:
        db.session.add(new_account)
        
        db.session.commit()
        print("New account created:", new_account)
    except Exception as e:
        return jsonify({"message": str(e)}), 400


    return jsonify({"message": "Account created!"}), 201



@app.route("/delete_post/<int:post_id>", methods = ["DELETE"])
def delete_post(post_id):
    post = Post.query.get(post_id)

    if not post:
        return jsonify({"message": "Post not found!"}), 404
    
    db.session.delete(post)
    db.session.commit()

    return jsonify({"message": "Post Deleted!"}), 200
    



if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(host='0.0.0.0', port=5001, debug=True)
    
        



























































# from flask import request, jsonify
# from config import app, db
# from models import Post

# @app.route("/allposts", methods= ["GET"])
# def get_posts():
#     allposts = Post.query.all()
#     json_allposts = list(map(lambda x: x.to_json(), allposts))
#     return jsonify(json_allposts) # just "allposts": was removed

# @app.route("/create_post", methods=["POST"])
# def create_post():
#     username = request.json.get("username")
#     description = request.json.get("description")
#     postType = request.json.get("postType")
#     mediaFilepath = request.json.get("mediaFilepath")
#     date = request.json.get("date")
#     location = request.json.get("location")
#     tags = request.json.get("tags")

#     if not username or not description or not postType or not date or not location:
#         return (
#             jsonify({"message": "You must include a username, description, date, post type and location"}),
#             400,
#         )

#     if not mediaFilepath and not tags:
#         new_post = Post(username = username, description = description, postType = postType, 
#                         date = date, location = location)
#     elif not mediaFilepath:
#         new_post = Post(username = username, description = description, postType = postType, 
#                         date = date, location = location, tags = tags)
#     elif not tags:
#         new_post = Post(username = username, description = description, postType = postType, 
#                         mediaFilepath = mediaFilepath, date = date, location = location)
#     else:
#         new_post = Post(username = username, description = description, postType = postType, 
#                         mediaFilepath = mediaFilepath, date = date, location = location,
#                         tags = tags)


#     try:
#         db.session.add(new_post)
#         db.session.commit()
#     except Exception as e:
#         return jsonify({"message": str(e)}), 400
    
#     return jsonify({"message": "Post added!"}), 201

# # @app.route("/update_post/<int:post_id>", methods = ["PATCH"])
# # def update_post(post_id):
# #     post = Post.query.get(post_id)

# #     if not post:
# #         return jsonify({"message": "Post not found!"}), 404
    
# #     data = request.json
# #     post.username = data.get("username", post.username)
# #     post.description = data.get("description", post.description)
# #     post.location = data.get("location", post.location)

# #     db.session.commit()

# #     return jsonify({"message": "Post updated!"}), 200

# @app.route("/delete_post/<int:post_id>", methods = ["DELETE"])
# def delete_post(post_id):
#     post = Post.query.get(post_id)

#     if not post:
#         return jsonify({"message": "Post not found!"}), 404
    
#     db.session.delete(post)
#     db.session.commit()

#     return jsonify({"message": "Post Deleted!"}), 200
    



# if __name__ == "__main__":
#     with app.app_context():
#         db.create_all()

#     app.run(host='0.0.0.0', port=5001, debug=True)
    
        