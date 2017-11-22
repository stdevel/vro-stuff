# SimplePamREST
This is a simple REST application written in Python, powered by [Flask](http://flask.pocoo.org). It can be used to manage passwords including IDs, names, descriptions, hostnames, usernames and passwords - wow such functionality. It also offers a shitty web interface for managing those information. This application is used in a workflow to access an external REST application (*link will follow soon*). This project is part of a tutorial about binding web applications to VMware vRealize Orchestrator using plug-ins or dynamic types (*blog link will follow soon*).

## Requirements
For using SimplePamREST, you will need:
- Python 2 or 3
- Flask
- SQLite3

## Usage
Simply start the script:
```
$ ./SimplePamREST.py
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
$ rm password.db
$ ./db.py
```

## API calls
The API implements the following calls:

| Call | Method | Description |
|:-----|:-------|:------------|
| ``/api/password/0`` | ``GET`` | Retrieves all password |
| ``/api/password/1`` | ``GET`` | Retrieves a password by ID |
| ``/api/password`` | ``POST`` | Creating a new password (*parameters using JSON*) |
| ``/api/password/1`` | ``PUT`` | Updates a password (*parameters using JSON*) |
| ``/api/password/1337`` | ``DELETE`` | Removes a password by ID |
| ``/api/password/0`` | ``GET`` | Retrieves a password by ID |

### Examples
Retrieving a password: ``GET /api/password/1``
```
{
 "results": [
 {
 "id": 1,
 "name": "demo1",
 "desc": "Demo password entry 1",
 "hostname": "localhost",
 "username": "admin",
 "password": "admin"
 }
 ]
}
```

Removing a password: ``DELETE /api/password/2``
```
{
 "message": "SUCCESS",
 "code": 0
}
```
