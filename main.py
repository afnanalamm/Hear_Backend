from flask import request, jsonify
from config import app, db
from models import Post

@app.route("/allposts", methods= ["GET"])
def get_posts():
    allposts = Post.query.all()
    json_allposts = list(map(lambda x: x.to_json(), allposts))
    return jsonify(json_allposts) # just "allposts": was removed

@app.route("/create_post", methods=["POST"])
def create_post():
    username = request.json.get("username")
    description = request.json.get("description")
    postType = request.json.get("postType")
    mediaFilepath = request.json.get("mediaFilepath")
    deadline = request.json.get("date")
    location = request.json.get("location")
    tags = request.json.get("tags")

    mediaAttached = request.json.get("mediaAttached")


    if not username or not description or not postType or not date or not location:
        return (
            jsonify({"message": "You must include a username, description, date, post type and location"}),
            400,
        )

    if not mediaFilepath and not tags:
        new_post = Post(username = username, description = description, postType = postType, 
                        date = deadline, location = location)
    elif not mediaFilepath:
        new_post = Post(username = username, description = description, postType = postType, 
                        date = deadline, location = location, tags = tags)
    elif not tags:
        new_post = Post(username = username, description = description, postType = postType, 
                        mediaFilepath = mediaFilepath, date = deadline, location = location)
    else:
        new_post = Post(username = username, description = description, postType = postType, 
                        mediaFilepath = mediaFilepath, date = deadline, location = location,
                        tags = tags)


    try:
        db.session.add(new_post)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    
    return jsonify({"message": "Post added!"}), 201

# @app.route("/update_post/<int:post_id>", methods = ["PATCH"])
# def update_post(post_id):
#     post = Post.query.get(post_id)

#     if not post:
#         return jsonify({"message": "Post not found!"}), 404
    
#     data = request.json
#     post.username = data.get("username", post.username)
#     post.description = data.get("description", post.description)
#     post.location = data.get("location", post.location)

#     db.session.commit()

#     return jsonify({"message": "Post updated!"}), 200

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
    
        