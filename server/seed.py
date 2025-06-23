from config import create_app, db
from models import User, Guest, Episode, Appearance
from faker import Faker
from datetime import datetime, timedelta
import random 

fake = Faker()
app = create_app()

with app.app_context():
    db.create_all()
    print("Seeding database with Faker...")

    Appearance.query.delete()
    Guest.query.delete()
    Episode.query.delete()
    User.query.delete()

    fake = Faker()
    print ("Creating !!!....")

    user = User(username="cristina")
    user.password_hash = "password123"
    db.session.add(user)

    guests = [
        Guest(name=fake.name(), occupation=fake.job())
        for _ in range(15)
    ]
    db.session.add_all(guests)

    base_date = datetime(2025, 6, 1)
    episodes = [
        Episode(number=i + 1, date=base_date + timedelta(days=i * 7))
        for i in range(5)
    ]
    db.session.add_all(episodes)
    db.session.commit()

    appearances = []
    for ep in episodes:
        for guest in random.sample(guests, k=3):
            appearances.append(
                Appearance(
                    guest_id=guest.id,
                    episode_id=ep.id,
                    rating=random.randint(1, 5)
                )
            )
    db.session.add_all(appearances)
    db.session.commit()

    print("Done seeding!")
