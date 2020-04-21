from flask import request, jsonify, current_app

from models.media import mediums, consumed_states

from logic.media import get_media, add_media, update_media, remove_media, get_media_by_id
from logic.user import get_user
from logic.login import login_required

# Note: It may seem like pluggable view with method based dispatching would make sense here. But because of how
# I implement login_required, and add a parameter logged_in_user, it would not work. The ViewMethod class would
# have methods that need to accept self as the first argument, which would screw up the login_required implementation


class UnauthorizedError(Exception):
    """
    UnauthorizedError results when a user tries to access something they don't have permission for
    usually results in 401 HTTP response
    """
    pass


@login_required
def media(logged_in_user, username):
    """
    media accepts a PUT request with JSON that matches
        {
            'id': a number representing the id of an existing media element to update
            'name': a string representing the name of the media to insert/update
            'medium': a string indicating the type of this media
                represents an Enum of possible values ('film', 'audio', 'literature', 'other')
            'consumed_state': a string indicating the current consumed state of this media
                represents an Enum of possible values ('not started', 'started', 'finished')
            'description': a string indicating some details about this media type (maximum 500 characters)
            'order': an integer indicating the order this media should be displayed on the frontend
        }
    or an array of JSON objects that matches the above (to update multiple items in one request)

    media accepts a GET request and returns all the media associated with the user specified by username
        a request arg 'consumed-state' can be set to 'not-started', 'started', or 'finished', and only media with the
            same consumed state will be returned
        a request arg 'medium' can be set to 'film', 'audio', 'literature', or 'other' and only media with the same
            medium will be returned
        if no request arg is present, all media will be returned

    media accepts a DELETE request with formdata that matches
        {
            'id': a number representing the id of the media to delete
        }
    """
    body = request.get_json()

    # This user is the one specified in url parameters, must match the auth token user
    user = get_user(username)
    validation_result = validate_url_username(logged_in_user, user)
    if validation_result is not None:
        return validation_result

    if request.method == 'GET':
        validation_result = validate_get_url_parameters()
        if validation_result is not None:
            return validation_result

        medium = request.args.get('medium')

        consumed_state = request.args.get('consumed-state')
        # 'not-started' is easier to put into url parameters than 'not started'
        if consumed_state == 'not-started':
            consumed_state = 'not started'

        media_list = get_media(username, medium, consumed_state)

        return jsonify({
            'success': True,
            'message': 'successfully got media for the logged in user',
            'data': [media.as_dict() for media in media_list]
        })
    elif request.method == 'PUT':
        if isinstance(body, list):
            # validate each media element in list before adding any of them
            for body_segment in body:
                validation_result = validate_put_body_parameters(body_segment)
                if validation_result is not None:
                    return jsonify({
                        'success': False,
                        'message': validation_result
                    }), 422

                if 'id' in body_segment:
                    media = get_media_by_id(body_segment['id'])
                    if media is None or media.user != user.id:
                        # If there is no media with this id, or it belongs to another user
                        return jsonify({
                            'success': False,
                            'message': 'logged in user doesn\'t have media with given id'
                        }), 401

            media_list = []

            for body_segment in body:
                # the validation in upsert_media_from_body is done above, so it can't throw an error
                media = upsert_media_from_body(body_segment, user)

                media_list.append(media.as_dict())

            return jsonify({
                'success': True,
                'message': 'successfully added/updated media elements',
                'data': media_list
            })
        else:
            try:
                media = upsert_media_from_body(body, user)
            except ValueError as e:
                return jsonify({
                    'success': False,
                    'message': str(e)
                }), 422
            except UnauthorizedError as e:
                return jsonify({
                    'success': False,
                    'message': str(e)
                }), 401

            return jsonify({
                'success': True,
                'message': 'successfully added/updated media element',
                'data': media.as_dict()
            })
    else:  # request.method == 'DELETE'
        validation_result = validate_delete_body_parameters(body)
        if validation_result is not None:
            return validation_result

        media = remove_media(body['id'])
        return jsonify({
            'success': True,
            'message': 'successfully deleted media element'
        })


def upsert_media_from_body(body, user):
    """
    upsert_media_from_body takes some dict that represents a media element and the user the media is for, and
    inserts/updates the media
    @param body: a python dict representing a media element
    @param user: the currently logged in user
    @return: The newly inserted/updated media element if there was no error, or a JSON response if there was an issue
        validating/inserting/updating the media
    """
    validation_result = validate_put_body_parameters(body)
    if validation_result is not None:
        raise ValueError(validation_result)

    medianame = None
    if 'name' in body:
        medianame = body['name']

    medium = None
    if 'medium' in body:
        medium = body['medium']

    consumed_state = None
    if 'consumed_state' in body:
        consumed_state = body['consumed_state']

    description = None
    if 'description' in body:
        description = body['description']

    order = None
    if 'order' in body:
        order = body['order']

    if 'id' in body:
        media = get_media_by_id(body['id'])
        if media is None or media.user != user.id:
            # If there is no media with this id, or it belongs to another user
            raise UnauthorizedError('logged in user doesn\'t have media with given id')

        media = update_media(body['id'], medianame, medium, consumed_state, description, order)
    else:
        media = add_media(user.id, medianame,
                          medium if medium is not None else 'other',
                          consumed_state if consumed_state is not None else 'not started',
                          description if description is not None else '',
                          order if order is not None else 0)

    return media


def validate_url_username(logged_in_user, url_user):
    """

    validate_url_username checks to see if url_user exists, and if it matches the logged_in_user.
    @param logged_in_user: a user model representing the currently logged in user
    @param url_user: a user model representing the user specified in the url
    @return: None if there is no issue, otherwise a JSON response with a detailed message on what was wrong
    """
    if url_user is None:
        # there is no user with this name, return incorrect parameters response
        return jsonify({
            'success': False,
            'message': 'user doesn\'t exist'
        }), 422

    if logged_in_user != url_user and not current_app.config['LOGIN_DISABLED']:
        # you can't get media for a user you are not logged in as
        return jsonify({
            'success': False,
            'message': 'not logged in as this user'
        }), 401


def validate_get_url_parameters():
    """
    validate_get_url_parameters checks the url parameters specified on a GET request
    @return: None if there is no issue, otherwise a JSON response with a detailed message on what was wrong
    """
    if 'consumed-state' in request.args and request.args.get('consumed-state') not in ['not-started', 'started', 'finished']:
        return jsonify({
            'success': False,
            'message': 'consumed-state url parameter must be \'not-started\', \'started\',  or \'finished\''
        }), 422

    if 'medium' in request.args and request.args.get('medium') not in mediums:
        return jsonify({
            'success': False,
            'message': 'medium url parameter must be \'film\', \'audio\', \'literature\', or \'other\''
        }), 422


def validate_put_body_parameters(body):
    """
    validate_put_body_parameters checks the body JSON, and makes sure the parameters are the correct type
    @return: None if there is no issue, otherwise a string with a detailed message on what was wrong
    """
    if 'id' not in body and 'name' not in body:
        # If id isn't in body, then this must be a new media element, and name is required
        return 'missing parameter \'name\' or parameter \'id\''

    if 'id' in body and not isinstance(body['id'], int):
        # return malformed parameters response if 'id' is not of type integer
        return 'id parameter must be type integer'

    if 'name' in body and not isinstance(body['name'], str):
        # return malformed parameters response if 'name' is not of type string
        return 'name parameter must be type string'

    if 'medium' in body and body['medium'] not in mediums:
        # return malformed parameters response if 'medium' isn't a valid medium type
        return 'medium parameter must be \'film\', \'audio\', \'literature\', or \'other\''

    if 'consumed_state' in body and body['consumed_state'] not in consumed_states:
        # return malfromed parameters response if 'consumed_state' isn't a valid consumed state
        return 'consumed_state parameter must be \'not started\', \'started\', or \'finished\''

    if 'description' in body and not isinstance(body['description'], str):
        # return malformed parameters response if 'description' isn't of type string
        return 'description parameter must be type string'

    if 'order' in body and not isinstance(body['order'], int):
        # TODO validate the range of this number?
        # return malformed parameters response if 'order' isn't of type int
        return 'order parameter must be type integer'


def validate_delete_body_parameters(body):
    """
    validate_delete_body_parameters checks the body JSON, and makes sure the parameters are the correct type
    @return: None if there is no issue, otherwise a JSON response with a detailed message on what was wrong
    """
    if 'id' not in body:
        # return malformed parameters response if 'id' isn't present
        return jsonify({
            'success': False,
            'message': 'missing parameter \'id\''
        }), 422
    elif not isinstance(body['id'], int):
        # return malformed parameters response if 'id' isn't of type integer
        return jsonify({
            'success': False,
            'message': 'id parameter must be type integer'
        }), 422
