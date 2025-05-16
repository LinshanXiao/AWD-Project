from app import create_app, db
from app.models import User, FriendRequest, Friendship, LeagueGame
import datetime


def populate_users():
    # Sample data to populate the user table
    users = [
        User(username="john_doe", password="password123", email="john@example.com", league_username="john_lol", valorant_username="john_val", PUBG_username="john_pubg", apex_username="john_apex", profile_image="no_profile_pic.jpg"),
        User(username="jane_smith", password="password123", email="jane@example.com", league_username="jane_lol", valorant_username="jane_val", PUBG_username="jane_pubg", apex_username="jane_apex", profile_image="no_profile_pic.jpg"),
        User(username="mike_ross", password="password123", email="mike@example.com", league_username="mike_lol", valorant_username="mike_val", PUBG_username="mike_pubg", apex_username="mike_apex", profile_image="no_profile_pic.jpg"),
        User(username="sarah_connor", password="password123", email="sarah@example.com", league_username="sarah_lol", valorant_username="sarah_val", PUBG_username="sarah_pubg", apex_username="sarah_apex", profile_image="no_profile_pic.jpg"),
        User(username="tony_stark", password="password123", email="tony@example.com", league_username="tony_lol", valorant_username="tony_val", PUBG_username="tony_pubg", apex_username="tony_apex", profile_image="no_profile_pic.jpg"),
        # New user with only username, password, and email
        User(username="minimal_user", password="simplepass", email="minimal@example.com", profile_image="no_profile_pic.jpg"),
    ]

    # Add users to the database
    db.session.add_all(users)
    db.session.commit()

    print("User table populated successfully!")

    # Create friend requests
    friend_requests = [
        FriendRequest(sender_id=users[2].id, receiver_id=users[0].id),  # mike_ross -> john_doe
        FriendRequest(sender_id=users[2].id, receiver_id=users[3].id),  # mike_ross -> sarah_connor
        FriendRequest(sender_id=users[4].id, receiver_id=users[0].id),  # tony_stark -> john_doe
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
        Friendship(user_id=users[0].id, friend_id=users[1].id),  # john_doe <-> jane_smith
        Friendship(user_id=users[1].id, friend_id=users[0].id),  # jane_smith <-> john_doe
        Friendship(user_id=users[0].id, friend_id=users[3].id),  # john_doe <-> sarah_connor
        Friendship(user_id=users[3].id, friend_id=users[0].id),  # sarah_connor <-> john_doe
    ]

    db.session.add_all(friendships)
    db.session.commit()

    print("Friendships created successfully!")

    # Create League game data only for users with a league_username
    games = []
    for user in users:
        if user.league_username:  # Only generate game data for users with a league_username
            for i in range(3):  # 3 games per user
                game = LeagueGame(
                    user_id=user.id,
                    game_id=i + 1,
                    date_played=datetime.datetime.now() - datetime.timedelta(days=i),
                    game_duration=f"{30 + i}m",
                    winning_team="Blue" if i % 2 == 0 else "Red",
                    league_username=user.league_username,
                    champion=f"Champion_{i + 1}",
                    kills=5 + i,
                    deaths=3 + i,
                    assists=7 + i,
                    kda=round((5 + i + 7 + i) / (3 + i), 2),
                    team="Blue" if i % 2 == 0 else "Red",
                )
                games.append(game)

    db.session.add_all(games)
    db.session.commit()

    print("League game data created successfully!")


if __name__ == "__main__":
    # Create the Flask app
    app = create_app()

    # Use the app context to access the database
    with app.app_context():
        populate_users()