# faker_data.py - Fixed and improved seeding script

from faker import Faker
from datetime import datetime
import random
import uuid
from config import app, db
from models import User, Address, Post, Comment

fake = Faker("en_GB")

# List of realistic topics
POST_TOPICS = [
    "climate change", "public transport improvement", "school funding", "animal rights",
    "mental health awareness", "plastic ban", "renewable energy", "local park renovation",
    "road safety", "affordable housing", "recycling program", "community center",
    "youth employment", "elderly care", "internet access in rural areas"
]

def get_random_image_url(topic):
    """Fallback to placeholder if internet/SSL issues"""
    placeholder = "https://via.placeholder.com/800x600?text=No+Image+Available"
    credit = "Placeholder image"

    # You can try Pexels (no key needed for basic use) or just use placeholder
    # Example with Pexels (free, no auth required for search):
    try:
        import requests
        query = topic.replace(" ", "+")
        url = f"https://pexels.com/search/{query}/"
        # Actually better: use a direct placeholder for reliability during seeding
        return placeholder, credit
    except:
        pass

    return placeholder, credit

def create_superuser():
    with app.app_context():
        if User.query.filter_by(emailAddress="admin@example.com").first():
            print("Superuser already exists – skipping.")
            return

        address = Address(
            addressLine1=fake.street_address(),
            city=fake.city(),
            state=fake.county(),
            postCode=fake.postcode()
        )
        db.session.add(address)
        db.session.flush()

        user = User(
            username="admin",
            firstName="Admin",
            lastName="User",
            dateOfBirth="1985-01-01",
            contactNumber="07123456789",
            emailAddress="admin@example.com",
            passwordHash="pbkdf2:sha256:600000$...your_hashed_password...",  # Use proper hash!
            superUser="true",
            createdOn=str(datetime.now()),
            addressID=address.addressID
        )
        db.session.add(user)
        db.session.commit()
        print("Superuser created.")

def create_fake_users(n=15):
    user_ids = []  # Store only IDs to avoid detached objects
    with app.app_context():
        for _ in range(n):
            address = Address(
                addressLine1=fake.street_address(),
                city=fake.city(),
                state=fake.county(),
                postCode=fake.postcode()
            )
            db.session.add(address)
            db.session.flush()

            # Use guaranteed unique email to avoid collisions
            email = f"user_{uuid.uuid4().hex[:12]}@example.com"

            user = User(
                username=fake.unique.user_name(),
                firstName=fake.first_name(),
                lastName=fake.last_name(),
                dateOfBirth=str(fake.date_of_birth(minimum_age=18, maximum_age=90)),
                contactNumber=fake.phone_number(),
                emailAddress=email,
                passwordHash=fake.password(length=60),
                superUser="false",
                createdOn=str(datetime.now()),
                addressID=address.addressID
            )
            db.session.add(user)
            db.session.flush()  # Get userID
            user_ids.append(user.userID)

        db.session.commit()
        print(f"Created {n} fake users.")
    return user_ids

def create_fake_posts(user_ids, n_posts_total=30):
    posts = []
    with app.app_context():
        for _ in range(n_posts_total):
            user_id = random.choice(user_ids)
            # Re-query user inside session to get username safely
            user = User.query.get(user_id)

            topic = random.choice(POST_TOPICS)
            title = f"Petition: {fake.sentence(nb_words=6).capitalize()}"

            image_url, credit = get_random_image_url(topic)

            post = Post(
                userID=user_id,
                username=user.username,  # Safe because queried inside session
                title=title,
                description=fake.paragraph(nb_sentences=8) + "\n\n" + credit,
                postType=random.choice(["petition", "news", "discussion"]),
                mediaAttached="true",
                mediaType="image",
                mediaURL=image_url,
                uniqueTitle_for_media=f"media_{fake.uuid4()[:8]}",
                interactionsID=str(uuid.uuid4()),
                location=fake.city(),
                deadline=str(fake.date_between(start_date='+30d', end_date='+180d')),
                tags=", ".join(fake.words(nb=5, unique=True)),
                createdOn=str(datetime.now()),
                approvalStatus=random.choice(["pending"]),
                approvedBy=user_id if random.random() > 0.3 else None,
                approvedOn=str(datetime.now()) if random.random() > 0.3 else None
            )
            db.session.add(post)
            db.session.flush()
            posts.append(post.postID)

        db.session.commit()
        print(f"Created {n_posts_total} fake posts.")
    return posts

def create_fake_comments(post_ids, min_comments=2, max_comments=8):
    with app.app_context():
        all_users = User.query.with_entities(User.userID, User.username).all()
        comment_count = 0

        for post_id in post_ids:
            num_comments = random.randint(min_comments, max_comments)
            for _ in range(num_comments):
                user_id, username = random.choice(all_users)

                comment = Comment(
                    postID=post_id,
                    userID=user_id,
                    username=username,
                    commentText=fake.paragraph(nb_sentences=random.randint(1, 3)),
                    createdOn=str(datetime.now())
                )
                db.session.add(comment)
                comment_count += 1

        db.session.commit()
        print(f"Created {comment_count} fake comments.")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    print("Seeding database...\n")

    create_superuser()

    fake_user_ids = create_fake_users(n=15)

    fake_post_ids = create_fake_posts(user_ids=fake_user_ids, n_posts_total=30)

    create_fake_comments(post_ids=fake_post_ids)

    print("\nSeeding complete!")