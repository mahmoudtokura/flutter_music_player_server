import datetime
from sqlalchemy import TEXT, VARCHAR, Column, DateTime
from models.base import Base


class Song(Base):
    __tablename__ = "songs"

    id = Column(TEXT, primary_key=True, index=True)
    song_url = Column(TEXT, index=True)
    thumbnail_url = Column(TEXT, index=True)
    song_title = Column(VARCHAR(100), index=True)
    artist = Column(TEXT, index=True)
    hex_code = Column(VARCHAR(6), index=True)
    added = Column(DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return f"<Song {self.song_title} by {self.artist}>"
