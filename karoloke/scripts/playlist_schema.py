from pydantic import BaseModel

class PlaylistItem(BaseModel):
    """
    Represents a karaoke playlist item.

    Attributes
    ----------
    filename : str
        Filename without the extension.
    artist : str
        Artist name.
    title : str
        Song title.
    part : str
        Song part.
    """
    filename: str
    artist: str
    title: str
    part: str
