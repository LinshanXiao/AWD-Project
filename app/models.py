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

    league_games: so.WriteOnlyMapped[list['League_Game_Instance']] = so.relationship(
        back_populates="users", secondary="league_game_player", lazy="dynamic"
    )

class League_Game_Instance(db.Model):
    __tablename__ = "league_game_instance"

    game_id: so.Mapped[int] = so.mapped_column(primary_key=True)
    date_played: so.Mapped[datetime.datetime] = so.mapped_column(nullable=False)
    game_duration: so.Mapped[datetime.time] = so.mapped_column(nullable=False)
    winning_team: so.Mapped[str] = so.mapped_column(sa.String(150), nullable=False)

    users: so.WriteOnlyMapped[list['User']] = so.relationship(
        back_populates="league_games", secondary="league_game_player"
    )

class League_Game_Player(db.Model):
    __tablename__ = "league_game_player"

    league_username: so.Mapped[str] = so.mapped_column(
        sa.String(150), sa.ForeignKey("user.league_username"), primary_key=True
    )
    game_id: so.Mapped[int] = so.mapped_column(
        sa.Integer, sa.ForeignKey("league_game_instance.game_id"), primary_key=True
    )
    champion: so.Mapped[str] = so.mapped_column(sa.String(150), nullable=False)
    kills: so.Mapped[int] = so.mapped_column(nullable=False)
    deaths: so.Mapped[int] = so.mapped_column(nullable=False)
    assists: so.Mapped[int] = so.mapped_column(nullable=False)
    kda: so.Mapped[float] = so.mapped_column(nullable=False)
    team: so.Mapped[str] = so.mapped_column(sa.String(150), nullable=False)

