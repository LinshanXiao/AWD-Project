from app import create_app, db
from app.models import User

def populate_users():
    # Sample data to populate the user table
    users = [
        User(username="john_doe", password="password123", email="john@example.com", league_username="john_lol", valorant_username="john_val", PUBG_username="john_pubg", apex_username="john_apex"),
        User(username="jane_smith", password="password123", email="jane@example.com", league_username="jane_lol", valorant_username="jane_val", PUBG_username="jane_pubg", apex_username="jane_apex"),
        User(username="mike_ross", password="password123", email="mike@example.com", league_username="mike_lol", valorant_username="mike_val", PUBG_username="mike_pubg", apex_username="mike_apex"),
        User(username="sarah_connor", password="password123", email="sarah@example.com", league_username="sarah_lol", valorant_username="sarah_val", PUBG_username="sarah_pubg", apex_username="sarah_apex"),
        User(username="tony_stark", password="password123", email="tony@example.com", league_username="tony_lol", valorant_username="tony_val", PUBG_username="tony_pubg", apex_username="tony_apex"),
    ]

    # Add users to the database
    db.session.add_all(users)
    db.session.commit()

    print("User table populated successfully!")

if __name__ == "__main__":
    app = create_app()  # Create the Flask application
    with app.app_context():  # Push the application context
        populate_users()