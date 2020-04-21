# GoGoMedia

tracks a users list of media they would like to consume, and what they have already consumed

## REQUIREMENTS                                                                                              

docker

## SETUP

1. `docker compose build`

2. `docker compuse up -d postgres` (creates postgres server, and initializes gogomedia DB)

3. `docker compose run --rm alembic upgrade head` (runs migrations on the gogomedia DB)

To connect to the PostgreSQL database running locally run:
`docker compose run --rm postgres psql -h postgres -U gogomedia_user --password gogomedia`
and then enter in `gogomedia_pass`

There should be a couple of tables if the alembic migrations ran correctly.

## Running                                                                                                   

`docker compose up -d gogomedia` to start the Flask server

## Testing

run `python run_tests.py` to run the tests

## Endpoints

Response Format:

```
{
    'success': True/False,
    'message': A string detailing what wen't wrong/right on the server,
    'data': Some JSON representing relevant data to the request,
    'auth_token': JWT authentication token returned from login endpoint
        Put the JWT authentication in headers of requests to endpoints
        that require login
}
```

- **/register [POST]** adds a new user
    
    Request Body:
    
    ```
    {
        'username': 'JohnSmith'
        'password': 'pass123'
    }
    ```
    
    Response Messages:
    
    - 422: 'missing parameter \'username\''
    - 422: 'missing parameter \'password\''
    - 422: 'username taken'
    - 201: 'user successfully registered'
    

- **/login [POST]** logs in a user

  Request Body:

  ```
  {
    'username': 'JohnSmith'
    'password': 'pass123'
  }
  ```

  Response Messages:
  
  - 422: 'missing parameter \'username\''
  - 422: 'missing parameter \'password''
  - 401: 'incorrect password'
  - 422: 'user doesn\'t exist'
  - 200: 'user successfully logged in'

- **/logout [GET] (login required)** logs a user out

  Response Messages:
  
  - 200: 'user successfully logged out'
                                                                                                             
- **/user/\<username>/media [PUT] (login required)** add/update a media element for this user

    Request Body:
    
    ```
    {
        'id': unique number
        'name': 'medianame',
        'medium': 'other'/'film'/'audio'/'literature' (optional),
        'consumed_state': 'not started'/'started'/'finished' (optional),
        'description': 'any string <= 500 characters' (optional)
    }
    ```
    
    Response Messages:
    
    - 422: 'missing parameter \'name\' or parameter \'id\''
    - 422: 'id parameter must be type integer'
    - 422: 'name parameter must be type string'
    - 422: 'medium parameter must be \'film\', \'audio\', \'literature\', or \'other\''
    - 422: 'consumed_state parameter must be \'not started\', \'started\', or \'finished\''
    - 422: 'user doesn\'t exist'
    - 422: 'description parameter must be type string'
    - 401: 'not logged in as this user'
    - 401: 'logged in user doesn\'t have media with given id'
    - 200: 'successfully added/updated media element'
    
- **/user/\<username>/media [GET] (login required)** get all media elements for this user

    Response Messages:
    
    - 422: 'user doesn\'t exist'
    - 401: 'not logged in as this user'
    - 200: 'successfully got media for the logged in user'

- **/user/\<username>/media?consumed-state=not-started/started/finished [GET] (login required)** get all consumed or unconsumed media elements for this user

    Response Messages:
    
    - 422: 'user doesn\'t exist'
    - 422: 'consumed-state url parameter must be \'not-started\', \'started\', or \'finished\''
    - 401: 'not logged in as this user'
    - 422: 'consumed url parameter must be \'yes\' or \'no\''
    - 200: 'successfully got media for the logged in user'

- **/user/\<username>/media?medium=other/film/audio/literature [GET] (login required)** get all media elements for this user of a specified medium type

    Response Messages:
    
    - 422: 'user doesn\'t exist'
    - 422: 'medium url parameter must be \'film\', \'audio\', \'literature\', or \'other\''
    - 401: 'not logged in as this user'
    - 422: 'medium url parameter must be \'film\', \'audio\', \'literature\', or \'other\''
    - 200: 'successfully got media for the logged in user'

- **/user/\<username>/media [DELETE] (login required)** delete a media element for this user

    Request Body:
    
    ```
    {
        'id': unique number
    }
    ```
    
    Response Messages:
    
    - 422: 'user doesn\'t exist'
    - 401: 'not logged in as this user'
    - 422: 'missing parameter \'id\''
    - 422: 'id parameter must be type integer'
    - 200: 'successfully deleted media element'

- **all login required endpoints**

    Request Headers:
    
    ```
    {
        'Authorization': 'JWT <auth token>'
    }
    ```
    
    Response Messages:
    - 422: 'authorization header malformed
    - 401: 'auth token blacklisted'
    - 401: 'signature expired'
    - 401: 'invalid token'
    - 401: 'no authorization header'

