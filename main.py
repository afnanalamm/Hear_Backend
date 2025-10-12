from flask import request, jsonify, send_from_directory
from config import app, db
import os
from werkzeug.utils import secure_filename
from models import *
from sqlalchemy import *
from datetime import datetime

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/check_login", methods=["POST"])
def check_login():
    try:
        login_data = request.json
        requestPasswordHash = login_data["passwordHash"]
        requestEmailAddress = login_data["emailAddress"]

        # Fetch user by email
        user = db.session.execute(
            select(User).where(User.emailAddress == requestEmailAddress)
        ).scalars().first()

        if user and user.passwordHash == requestPasswordHash:
            return jsonify({"message": "Login successful"}), 200
        else:
            return jsonify({"message": "Incorrect Attempt"}), 400

    except Exception as e:
        return jsonify({"message": str(e)}), 400

        

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
        "createdOn": datetime.now()

        # firstName: firstName,
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
    new_account = User(**{k: v for k, v in account_data.items()}) # Only include non-None values. This avoids multiple conditionals. This uses dictionary unpacking.

  
    try:
        db.session.add(new_account)
        
        db.session.commit()
        print("New account created:", new_account)
    except Exception as e:
        return jsonify({"message": str(e)}), 400


    return jsonify({"message": "Account created!"}), 201
  
    

@app.route("/allposts", methods= ["GET"])
def get_posts():
    allposts = Post.query.all()

    json_allposts = (list(map(lambda x: x.to_json(), allposts)))
    lastToFirst_allposts = json_allposts[::-1]

    return jsonify(lastToFirst_allposts), 200


@app.route("/create_post", methods=["POST"])
def create_post():
    data = request.json
    # required_fields = ["userID", "description", "postType", "deadline", "location", "title"]
    
    # # Check for required fields
    # if not all(data.get(field) for field in required_fields):
    #     return jsonify({"message": "Missing required fields: Description, deadline, location, title"}), 400

    # Prepare post data
    post_data = {
        "userID": data["userID"],
        "title": data["title"],
        
        "description": data["description"],
        "postType": data["postType"],
        "deadline": data["deadline"],
        "location": data["location"],
        "mediaURL": secure_filename(data["mediaURL"]),
        "tags": data["tags"],
        "createdOn": datetime.now()
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


@app.route('/upload_media', methods=['POST'])
def upload_image():
    if 'media' not in request.files:
        return jsonify({'message': 'No media provided'}), 400

    image = request.files['media']
    mediaURL = secure_filename(image.filename)
    save_path = os.path.join(UPLOAD_FOLDER, mediaURL)
    image.save(save_path)

    # Construct URL (assuming backend runs on port 5001)
    file_url = f"http://localhost:5001/{UPLOAD_FOLDER}/{mediaURL}"
    return jsonify({'url': file_url}), 200



@app.route('/uploads/<path:mediaURL>')
def serve_uploaded_file(mediaURL):
    return send_from_directory(UPLOAD_FOLDER, mediaURL)


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