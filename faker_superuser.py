# seed_superuser.py
from faker import Faker
from datetime import datetime
from config import app, db
from models import User, Address

fake = Faker("en_GB")

def create_superuser():
    with app.app_context():
        address = Address(
            addressLine1=fake.street_address(),
            addressLine2=None,
            city=fake.city(),
            state=fake.county(),
            postCode=fake.postcode()
        )
        db.session.add(address)
        db.session.flush()  # get addressID

        user = User(
            username=fake.unique.user_name(),
            firstName=fake.first_name(),
            lastName=fake.last_name(),
            dateOfBirth=str(fake.date_of_birth(minimum_age=18, maximum_age=128)),
            contactNumber=fake.phone_number(),
            emailAddress= "z",
            passwordHash= "594e519ae499312b29433b7dd8a97ff068defcba9755b6d5d00e84c524d67b06",#fake.password(length=256),  # replace with hash of you chosen pswrd
            superUser="true",
            createdOn=str(datetime.now()),
            addressID=address.addressID
        )

        db.session.add(user)
        db.session.commit()

        print("Superuser created:", user.to_json())

if __name__ == "__main__":
    create_superuser()
