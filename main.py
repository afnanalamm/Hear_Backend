from flask import request, jsonify, send_from_directory
from config import *
import os
from werkzeug.utils import secure_filename
from models import *
from sqlalchemy import *
from datetime import datetime
from urllib.parse import unquote

    # All of my searching algorithms have a best case time complexity of O(n).
    # This can become a performance bottleneck with large number of posts and votes.
    # I will have to optimize this in future by using better database queries.
    # Alternatively, I will try to implement hashing techniques to speed up searches.



UPLOAD_FOLDER = 'uploads' # constant name for for folder to store all uploaded media files
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/check_login", methods=["POST"]) # rudimentary login check function
def check_login():
    try:
        login_data = request.json
        requestPasswordHash = login_data["passwordHash"]
        requestEmailAddress = login_data["emailAddress"]

        # Fetch user by email
        user = db.session.execute(
            select(User).where(User.emailAddress == requestEmailAddress)
        ).scalars().first() # Get the first matching user        

        if user and user.passwordHash == requestPasswordHash: # Compare password hashes
            access_token = create_access_token(identity=str(user.userID)) # this was causing the error.
            
            # user.userID is an integer (1), but Flask-JWT-Extended expects the identity (sub) to be a string by default in newer versions.
            # When @jwt_required() runs on /allposts, it tries to do:
            # emailAddress = get_jwt_identity()
            # But since sub is a number (1), not a string, it fails validation with:
            # "Subject must be a string"
            # → Returns 422 with {"msg": "Subject must be a string"}

            print("User logged in:", user)

            return jsonify({
                "access_token": access_token
            }), 200

            return jsonify({"message": "Login successful", "userID": user.userID}), 200 # Send successful login response
        else:
            return jsonify({"message": "Incorrect Attempt"}), 400

    except Exception as e:
        return jsonify({"message": str(e)}), 400
    

        

@app.route("/create_account", methods=["POST"]) # create new user account
def create_account():
    data = request.json
    required_fields = ["firstName", "lastName", "dateOfBirth", "contactNumber", "emailAddress", "username"] 
    # can't create account without these fields
    
    (
        # Check for required fields
    # if not all(data.get(field) for field in required_fields):
    #     return jsonify({"message": "Missing required fields: Description, deadline, location"}), 400

    # create new account
    )
    account_data = { # prepare account data, to be used to create new account object

        "username": data["username"],
        "firstName": data["firstName"],
        "lastName": data["lastName"],
        "dateOfBirth": data["dateOfBirth"],
        "contactNumber": data["contactNumber"],
        "emailAddress": data["emailAddress"],

        "passwordHash": data["passwordHash"],
        "superUser": data["superUser"],
        "createdOn": datetime.now()


        # firstName: firstName, # commented out lines are to be used in future for more detailed user profiles
        # lastName: lastName,
        # username: username,
        # dateOfBirth: dateOfBirth,
        # emailAddress: emailAddress,
        # contactNumber: contactNumber,
        # passwordHash: passwordHash,
        # addressLine1: addressLine1,
        # addressLine2: addressLine2,
        # city: city,
        # postCode: postCode,
        # country: country,
        # superUser: superUser,
    }

    # Create new post
    new_account = User(**{k: v for k, v in account_data.items()}) 

    # Only include non-None values. This avoids multiple conditionals. This uses dictionary unpacking.

  
    try:
        db.session.add(new_account) # add new account to database
        
        db.session.commit()
        print("New account created:", new_account.to_json())
    except Exception as e:
        return jsonify({"message": str(e)}), 400


    return jsonify({"message": "Account created!"}), 201
  
    


@app.route("/allposts", methods=["GET"])
@jwt_required()
def get_posts():
    userID_str = get_jwt_identity()  # e.g. "1"
    userID = int(userID_str)

    allposts = Post.query.all()
    json_allposts = [post.to_json() for post in allposts]
    json_allposts.reverse()

    result = []

    for post in json_allposts:
        user_reaction = Reaction.query.filter_by(
            postID=post["postID"],
            userID=userID
        ).first()

        post["currentUserID"] = userID

        if user_reaction:
            post["userHasVoted"] = True
            post["userVoteType"] = user_reaction.reactionType
        else:
            post["userHasVoted"] = False
            post["userVoteType"] = None

        result.append(post)

    return jsonify(result), 200

@app.route("/create_post", methods=["POST"])
@jwt_required()
def create_post():
    data = request.get_json()
    userID_str = get_jwt_identity()
    userID = int(userID_str)
    (
        # required_fields = ["userID", "description", "postType", "deadline", "location", "title"]
    
    # # Check for required fields
    # if not all(data.get(field) for field in required_fields):
    #     return jsonify({"message": "Missing required fields: Description, deadline, location, title"}), 400
    )
    # Prepare post data
    post_data = {
        "userID": userID,
        "title": data["title"],
        "uniqueTitle_for_media": data["uniqueTitle_for_media"], # unique title for media file, to avoid conflicts
        
        "description": data["description"],
        "postType": data["postType"],
        "deadline": data["deadline"],
        "location": data["location"],
        "mediaURL": secure_filename(data["mediaURL"]), # got rid of the secure_filename() here as it was causing issues with URLs. Same thing below
        "tags": data["tags"],
        "createdOn": datetime.now()
    }

    # Create new post
    new_post = Post(**{k: v for k, v in post_data.items()})

    # During refactoring, I had added "if v is not None" to filter out None values, 
    # but I removed it as it was creating an SQL IntegrityError due to NOT NULL constraints on posts.createdOn
    # If needed in future, can re-add with better conditional checks.

    print("New post to be added:", new_post.to_json())      

    try:
        db.session.add(new_post)
        
        db.session.commit()
        print("New post added:", new_post)
    except Exception as e:
        return jsonify({"message": str(e)}), 400
        
    
    return jsonify({"message": "Post added!"}), 201


@app.route('/upload_media', methods=['POST']) # upload media file endpoint
def upload_image():
    if 'media' not in request.files:
        return jsonify({'message': 'No media provided'}), 400

    image = request.files['media']
    filename = secure_filename(image.filename) 
    save_path = os.path.join(UPLOAD_FOLDER, filename)
    image.save(save_path)

    file_url = f"http://localhost:5001/uploads/{filename}"
    return jsonify({'url': file_url}), 200



@app.route('/uploads/<filename>')
def serve_uploaded_file(filename):
    # secure_filename was already used on upload - safe to serve directly
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route("/vote", methods=["POST"])
@jwt_required()
def vote():
    """
    Receives vote from frontend: Agree or Disagree
    Records postID, userID (from JWT), reactionType ("agree"/"disagree")
    """
    try:
        data = request.json
        postID = data.get("postID")
        action = data.get("reactionType")  # "agree" or "disagree"

        if not postID or not action:
            return jsonify({"message": "Missing postID or reactionType"}), 400

        # Get userID directly from JWT (it's a string like "1")
        userID_str = get_jwt_identity()
        userID = int(userID_str)  # Convert to int for database query

        # Check if user already voted on this post
        existing_vote = Reaction.query.filter_by(postID=postID, userID=userID).first()

        # If same vote exists, remove it (toggle off)
        if existing_vote and existing_vote.reactionType == action:
            db.session.delete(existing_vote)
            db.session.commit()

            agree_count = Reaction.query.filter_by(postID=postID, reactionType="agree").count()
            disagree_count = Reaction.query.filter_by(postID=postID, reactionType="disagree").count()

            return jsonify({
                "message": f"You just stopped {action}ing",
                "agreeCount": agree_count,
                "disagreeCount": disagree_count,
                "userHasVoted": False,
                "userVoteType": None
            }), 200

        # Otherwise, create new vote
        new_reaction = Reaction(
            postID=postID,
            userID=userID,
            reactionType=action,
            timestamp=datetime.utcnow()
        )

        db.session.add(new_reaction)
        db.session.commit()

        # Get updated counts
        agree_count = Reaction.query.filter_by(postID=postID, reactionType="agree").count()
        disagree_count = Reaction.query.filter_by(postID=postID, reactionType="disagree").count()

        print(f"[{action.upper()}] Post {postID} by user {userID} at {new_reaction.timestamp}")

        return jsonify({
            "message": "You have Voted",
            "postID": postID,
            "agreeCount": agree_count,
            "disagreeCount": disagree_count,
            "userHasVoted": True,
            "userVoteType": action
        }), 200

    except Exception as e:
        db.session.rollback()
        print("Vote error:", str(e))
        return jsonify({"message": str(e)}), 500

@app.route("/allcomments", methods=["GET"])
@jwt_required()
def get_comments():
    try:
        userID_str = get_jwt_identity()  # still validated by JWT
        postID = request.args.get("postID", type=int)

        if not postID:
            return jsonify({"message": "postID query parameter is required"}), 400

        comments = Comment.query.filter_by(postID=postID).all()
        comments_json = [comment.to_json() for comment in comments]

        return jsonify(comments_json), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500


@app.route("/create_comment", methods=["POST"])
@jwt_required()
def create_comment():
    data = request.get_json()
    userID_str = get_jwt_identity()
    userID = int(userID_str)


    try:

        data = request.json
        postID = data.get("postID")
        commentText = data.get("commentText")
        createdOn = datetime.now()

        # Prepare comment data
        new_comment = Comment(
            postID = postID,
            userID = userID,
            commentText = commentText,
            createdOn = createdOn
        )
        db.session.add(new_comment)
        
        db.session.commit()
        print("New comment added:", new_comment)
    except Exception as e:
        return jsonify({"message": str(e)}), 400
        
    
    return jsonify({"message": "Comment added!"}), 201


@app.route("/delete_post/<int:post_id>", methods = ["DELETE"]) 
# delete post by post ID. Not yet integrated into frontend, but kept from the Youtube tutorial.
def delete_post(post_id):
    post = Post.query.get(post_id)

    if not post:
        return jsonify({"message": "Post not found!"}), 404
    
    db.session.delete(post)
    db.session.commit()

    return jsonify({"message": "Post Deleted!"}), 200
    


# Run the Flask app
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(host='0.0.0.0', port=5001, debug=True)