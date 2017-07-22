# FlaskREST
This is a simple REST application written in Python, powered by [Flask](http://flask.pocoo.org). It's magicness results in managing users with IDs, names and mail addresses - wow such functionality. It also offers a shitty web interface for managing those information. This application is used in a workflow to access an external REST application (*link will follow soon*). This project is part of a tutorial about developing web applications in python - [check it out on my blog](http://st-devel.net/pfar).

## Requirements
For using FlaskREST, you will need:
- Python 2 or 3
- Flask
- SQLite3

## Usage
Simply start the script: 
```
$ ./FlaskREST.py
 * Running on http://localhost:5000/
 ```

Hitting **CTRL+C** will gracefully close the database.

To make FlaskREST listen on other interfaces as well, edit the last lines of code:
```
...
#enable if you also like to live dangerously
app.run(debug=False, host="0.0.0.0")
#app.run(debug=False)
```

Open http://localhost:5000/ to access the web interface for managing users.

If you want to recreate the demo database, remove it and execute ``db.py``:
```
$ rm users.db
$ ./db.py
```
 
## API calls
The API implements the following calls:

| Call | Method | Description |
|:-----|:-------|:------------|
| ``/api/user/0`` | ``GET`` | Retrieves all users |
| ``/api/user/1`` | ``GET`` | Retrieves an user by ID |
| ``/api/user`` | ``POST`` | Creating a new user (*parameters using JSON*) |
| ``/api/user/1`` | ``PUT`` | Updates an user (*parameters using JSON*) |
| ``/api/user/1337`` | ``DELETE`` | Removes an user by ID |
| ``/api/user/0`` | ``GET`` | Retrieves an user by ID |

### Examples
Retrieving an user: ``GET /api/user/1``
```
{
 "results": [
 {
 "mail": "giertz@shittyrobots.loc",
 "id": 1,
 "name": "Simone Giertz"
 }
 ]
}
```

Removing an user: ``DELETE /api/user/2``
```
{
 "message": "SUCCESS",
 "code": 0
}
```
