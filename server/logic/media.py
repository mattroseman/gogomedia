from database import db

from models.media import Media
from models.user import User


def add_media(userid, medianame, medium='other', consumed_state='not started', description='', order=0):
    """
    add_media creates a new media record with the given medianame and assigns the media to the user with the given
    username
    """
    media = Media(medianame, userid, medium, consumed_state, description, order)
    db.session.add(media)
    db.session.commit()

    return media


def update_media(id, medianame=None, medium=None, consumed_state=None, description=None, order=None):
    """
    upadte_media updates an existing media record with the given id
    @param id: id is required when updating
    @param: if the given parameter's are None or missing no change is made to that media property
    """
    media = Media.query.filter_by(id=id).first()

    if medianame is not None:
        media.medianame = medianame
    if consumed_state is not None:
        media.consumed_state = consumed_state
    if medium is not None:
        media.medium = medium
    if description is not None:
        media.description = description
    if order is not None:
        media.order = order
    db.session.commit()

    return media


def remove_media(id):
    """
    remove_media removes a Media record from the database
    """
    # if there is no record for this medianame for this user, then filter returns nothing, and nothing is deleted
    Media.query.filter_by(id=id).delete()
    db.session.commit()


def get_media(username, medium=None, consumed_state=None):
    """
    get_media returns all the media associated with the given username.
    If medium is set to a medium type, then only the media with the same medium type will be returned.
    If consumed_state is set to a consumed_state, then only the media with the same consumed_state will be returned.
    @return: a list of media elements
    """
    media_list = User.query.filter_by(username=username).first().media

    # if medium is set then only return the media items that have the same medium type
    if medium is not None:
        media_list = [media for media in media_list if media.medium == medium]

    # if consumed is set then only return the media items that have the same consumed value
    if consumed_state is not None:
        media_list = [media for media in media_list if media.consumed_state == consumed_state]

    return media_list


def get_media_by_id(id):
    """
    get_media_by_id returns a single media object with the given id, or None if there is no media with the given id
    """
    return Media.query.filter_by(id=id).first()
