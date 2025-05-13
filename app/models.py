import datetime
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from flask_login import UserMixin

class User(UserMixin,db.Model):
    __tablename__ = "user"
    id : so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(150), unique=True, nullable=False)
    password: so.Mapped[str] = so.mapped_column(sa.String(150), nullable=False)
    email: so.Mapped[str] = so.mapped_column(sa.String(150), unique=True, nullable=False)
    league_username: so.Mapped[str | None] = so.mapped_column(sa.String(150), unique=True, nullable=True)
    valorant_username: so.Mapped[str | None] = so.mapped_column(sa.String(150), unique=True, nullable=True)
    PUBG_username: so.Mapped[str | None] = so.mapped_column(sa.String(150), unique=True, nullable=True)
    apex_username: so.Mapped[str | None] = so.mapped_column(sa.String(150), unique=True, nullable=True)

    #relationships
    games: so.Mapped[list['LeagueGame']] = so.relationship(back_populates="user")

class LeagueGame(db.Model):
    __tablename__ = "league_game"

    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)

    # Optional foreign key to User
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("user.id"), nullable=True)

    # Game info
    game_id: so.Mapped[int] = so.mapped_column(nullable=False)
    date_played: so.Mapped[datetime.datetime] = so.mapped_column(nullable=False)
    game_duration: so.Mapped[str] = so.mapped_column(sa.String(20), nullable=False)
    winning_team: so.Mapped[str] = so.mapped_column(sa.String(150), nullable=False)

    # Player info
    league_username: so.Mapped[str] = so.mapped_column(sa.String(150), nullable=False)
    champion: so.Mapped[str] = so.mapped_column(sa.String(150), nullable=False)
    kills: so.Mapped[int] = so.mapped_column(nullable=False)
    deaths: so.Mapped[int] = so.mapped_column(nullable=False)
    assists: so.Mapped[int] = so.mapped_column(nullable=False)
    kda: so.Mapped[float] = so.mapped_column(nullable=False)
    team: so.Mapped[str] = so.mapped_column(sa.String(150), nullable=False)

    # Relationship (backref for convenience)
    user: so.Mapped['User'] = so.relationship(back_populates="games")



class Friendship(db.Model):
    __tablename__ = "friendship"

    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'), nullable=False)
    friend_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'), nullable=False)

    __table_args__ = (
        sa.UniqueConstraint('user_id', 'friend_id', name='unique_friendship'),
    )


class FriendRequest(db.Model):
    __tablename__ = "friend_request"

    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    sender_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'), nullable=False)
    receiver_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'), nullable=False)

    __table_args__ = (
        sa.UniqueConstraint('sender_id', 'receiver_id', name='unique_friend_request'),
    )