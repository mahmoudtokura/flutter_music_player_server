import datetime
from sqlalchemy import TEXT, Column, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base
from models.song import Song
from models.user import User


class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(TEXT, primary_key=True, index=True)
    song_id = Column(TEXT, ForeignKey(Song.id), index=True)
    user_id = Column(TEXT, ForeignKey(User.id), index=True)
    added = Column(DateTime, default=datetime.datetime.now)

    song = relationship("Song")
    user = relationship("User", back_populates="favorites")

    def __repr__(self):
        return f"<Favorite {self.song_id} by {self.user_id}>"
