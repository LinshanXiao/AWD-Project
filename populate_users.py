from app import create_app, db
from app.models import User, FriendRequest, Friendship



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

    # Create friend requests
    friend_requests = [
        FriendRequest(sender_id=users[2].id, receiver_id=users[0].id),  # john_doe -> jane_smith
        FriendRequest(sender_id=users[2].id, receiver_id=users[3].id),  # mike_ross -> sarah_connor
        FriendRequest(sender_id=users[4].id, receiver_id=users[0].id),  # john_doe -> jane_smith
    ]

    db.session.add_all(friend_requests)
    db.session.commit()

    print("Friend requests created successfully!")

    # Create friendships
    friendships = [
        Friendship(user_id=users[0].id, friend_id=users[4].id),  # john_doe <-> tony_stark
        Friendship(user_id=users[4].id, friend_id=users[0].id),  # tony_stark <-> john_doe
        Friendship(user_id=users[1].id, friend_id=users[3].id),  # jane_smith <-> sarah_connor
        Friendship(user_id=users[3].id, friend_id=users[1].id),  # sarah_connor <-> jane_smith
        Friendship(user_id=users[0].id, friend_id=users[1].id),  # john_doe <-> tony_stark
        Friendship(user_id=users[1].id, friend_id=users[0].id),  # tony_stark <-> john_doe
        Friendship(user_id=users[0].id, friend_id=users[3].id),  # jane_smith <-> sarah_connor
        Friendship(user_id=users[3].id, friend_id=users[0].id),  # sarah_connor <-> jane_smith
    ]

    db.session.add_all(friendships)
    db.session.commit()

    print("Friendships created successfully!")

if __name__ == "__main__":
    app = create_app()  # Create the Flask application
    with app.app_context():  # Push the application context
        populate_users()