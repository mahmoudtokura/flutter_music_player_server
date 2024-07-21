import uuid
from fastapi import APIRouter, Depends, File, UploadFile, Form, status
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
import cloudinary
import cloudinary.uploader

from database import get_db
from middleware.auth_middleware import auth_middleware
from models.favorite import Favorite
from models.song import Song
from pydantic_schemas.favorite_song import FavoriteSong

router = APIRouter()

# Configuration
cloudinary.config(
    cloud_name="sssssssss",
    api_key="xxxxxxxxxx",
    api_secret="xxxxxxxxx",  # Click 'View Credentials' below to copy your API secret
    secure=True,
)


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_song(
    song: UploadFile = File(...),
    thumbnail: UploadFile = File(...),
    artist: str = Form(...),
    song_title: str = Form(...),
    hex_code: str = Form(...),
    db: Session = Depends(get_db),
    auth_dict: str = Depends(auth_middleware),
):
    try:
        print("Uploading files...")
        # Upload an song
        song_id = f"song_id_{str(uuid.uuid4())}"
        song_result = cloudinary.uploader.upload(
            song.file,
            resource_type="auto",
            folder=f"songs/{song_id}",
        )
        thumbnail_result = cloudinary.uploader.upload(
            thumbnail.file,
            resource_type="image",
            folder=f"songs/{song_id}",
        )

        new_song = Song(
            id=song_id,
            song_url=song_result["url"],
            thumbnail_url=thumbnail_result["url"],
            song_title=song_title,
            artist=artist,
            hex_code=hex_code,
        )

        db.add(new_song)
        db.commit()
        db.refresh(new_song)
        return new_song
    except Exception as e:
        print(e)
        return {"error": "An error occurred"}


@router.get("/list")
def list_songs(
    db: Session = Depends(get_db), auth_dict: str = Depends(auth_middleware)
):
    songs = db.query(Song).all()
    return songs


@router.get("/list/favorites")
def list_user_favorite_songs(
    db: Session = Depends(get_db), auth_dict: str = Depends(auth_middleware)
):
    user_id = auth_dict["uid"]
    songs = (
        db.query(Favorite)
        .filter(Favorite.user_id == user_id)
        .options(joinedload(Favorite.song))
        .all()
    )
    return songs


@router.post("/favorite")
def favorite_song(
    fav_song: FavoriteSong,
    db: Session = Depends(get_db),
    auth_dict: str = Depends(auth_middleware),
):
    user_id = auth_dict["uid"]
    print(user_id)
    song = (
        db.query(Favorite)
        .filter(Favorite.song_id == fav_song.song_id, Favorite.user_id == user_id)
        .first()
    )
    if song:
        db.delete(song)
        db.commit()
        return {"message": False}

    new_favorite = Favorite(
        id=f"favorite_id_{str(uuid.uuid4())}",
        song_id=fav_song.song_id,
        user_id=user_id,
    )
    db.add(new_favorite)
    db.commit()
    db.refresh(new_favorite)
    return {"message": True}
