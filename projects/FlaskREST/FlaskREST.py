#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A simple Flask-based user management application that might be used for demos.
"""
import json
import sqlite3
import atexit
from flask import Flask, request, Response, render_template
APP = Flask(__name__)

#DB_CONN = None
#DB_CUR = None
#TODO: implement database class to avoid globals?



#GENERIC FUNCTIONS
def shutdown():
    """
    This function ensures the database is gracefully closed when
    shutting down the application.
    """
    global DB_CONN

    #close database
    DB_CONN.commit()
    DB_CONN.close()
    print("Graceful shutdown, bye!")

def get_data(data):
    """
    This function deserializes an JSON object.

    :param data: JSON data
    :type data: str
    """
    json_data = json.loads(data)
    print("Deserialized data: {}".format(data))
    return json_data

def return_result(result):
    """
    This function simply returns an operation's status in JSON.

    :param result: boolean whether successful
    :type result: bool
    """
    ret = {}
    if result:
        ret["code"] = 0
        ret["message"] = "SUCCESS"
    else:
        ret["code"] = 1
        ret["message"] = "FAILURE"
    return json.dumps(ret)



#DATABASE FUNCTIONS
#TODO: creating and editing users in ONE function?
def user_create(user_id, user_name, user_mail):
    """
    This function creates an user.

    :param user_id: user ID
    :type user_id: int
    :param user_name: user name
    :type user_name: str
    :param user_mail: user mail
    :type user_mail: str
    """
    global DB_CONN
    global DB_CUR

    try:
        DB_CUR.execute(
            """INSERT INTO users (user_id, user_name, user_mail)
            VALUES (?, ?, ?)""",
            (user_id, user_name, user_mail)
        )
        DB_CONN.commit()
        print(
            "Added user #{} with name={},mail={}".format(
                user_id, user_name, user_mail
            )
            )
        return True
    except Exception as err:
        print("Unable to create user #{} with name={},mail={}: {}".format(
            user_id, user_name, user_mail, err
        ))
        return False

def user_update(user_id, user_newid, user_name, user_mail):
    """
    This function updates an user.

    :param user_id: user ID
    :type user_id: int
    :param user_name: user name
    :type user_name: str
    :param user_mail: user mail
    :type user_mail: str
    """
    global DB_CONN
    global DB_CUR

    try:
        DB_CUR.execute(
            """UPDATE users SET user_id=?, user_name=?, user_mail=?
            WHERE user_id=?""", (
                user_newid, user_name, user_mail, user_id
            )
        )
        DB_CONN.commit()
        print(
            "Updated user #{} with id={},name={},mail={}".format(
                user_id, user_newid, user_name, user_mail
            )
            )
        return True
    except Exception as err:
        print("Unable to update user #{} with id={},name={},mail={}: {}".format(
            user_id, user_newid, user_name, user_mail, err
        ))
        return False

def user_remove(user_id):
    """
    This function removes an user.

    :param user_id: user ID
    :type user_id: int
    """
    global DB_CONN
    global DB_CUR

    print("About to remove user #{}".format(user_id))
    try:
        DB_CUR.execute(
            "DELETE FROM users WHERE user_id=?",
            (user_id,)
        )
        DB_CONN.commit()
        #check whether an user was removed
        if DB_CUR.rowcount > 0:
            print("Removed user #{}".format(user_id))
            return True
        return False
    except Exception as err:
        print("Unable to remove user #{}: {}".format(
            user_id, err
        ))
        return False

def user_get(user_id):
    """
    This function retrieves a user's information.

    :param user_id: user ID
    :type user_id: int
    """
    global DB_CUR

    #execute database query
    if user_id > 0:
        #return all users
        DB_CUR.execute(
            "SELECT * FROM users WHERE user_id=?;",
            (user_id,)
        )
    else:
        #return one particular user
        DB_CUR.execute("SELECT * FROM users;")

    #prepare result
    json = {}
    results = []
    temp = {}
    #get _all_ the information
    for row in DB_CUR:
        temp[row[0]] = {}
        temp[row[0]]["id"] = row[0]
        temp[row[0]]["name"] = row[1]
        temp[row[0]]["mail"] = row[2]
        results.append(temp[row[0]])
    json["results"] = results
    return json



#FLASK FRONTEND FUNCTIONS
@APP.route("/")
def index():
    """
    This function simply presents the main page.
    """
    return render_template("index.html")

@APP.route("/user/create", methods=["GET", "POST"])
def form_create():
    """
    This function presents the form to create users and returns the API result.
    """
    if request.method == "POST":
        #create user
        if user_create(
                request.form["id"], request.form["name"], request.form["mail"]
            ):
            return "User created!"
        return "User could not be created!"
    else:
        #show form
        return render_template("create.html")

@APP.route("/user/", methods=["GET"])
def form_users():
    """
    This function lists all users.
    """
    #get _all_ the users
    users = user_get(0)
    #render users in HTML template
    return render_template("users.html", result=users)

@APP.route("/user/<int:user_id>", methods=["GET"])
def form_user(user_id):
    """
    This function displays a particular user.

    :param user_id: user ID
    :type user_id: int
    """
    #display a particular users
    result = user_get(user_id)["results"][0]
    return render_template("user.html", user=result)

@APP.route("/user/delete/<int:user_id>", methods=["GET"])
def from_delete(user_id):
    """
    This function deletes a particular user.

    :param user_id: user ID
    :type user_id: int
    """
    #try to delete user
    if user_delete(user_id):
        return "User deleted!"
    return "User could not be deleted!"

@APP.route("/user/edit/<int:user_id>", methods=["GET", "POST"])
def form_edit(user_id):
    """
    This function presents the form to edit users and returns form
    data to the API.

    :param user_id: user ID
    :type user_id: int
    """
    if request.method == "POST":
        #edit user
        if user_update(
                user_id, request.form["id"], request.form["name"],
                request.form["mail"]
            ):
            return "User edited!"
        return "User could not be edited!"
    else:
        #show form, preselect values
        try:
            result = user_get(user_id)["results"][0]
            return render_template("edit.html", user=result)
        except IndexError:
            return render_template("nonexist.html")



#FLASK API FUNCTIONS
@APP.route("/api/user/<int:user_id>", methods=["GET"])
def user_show(user_id):
    """
    This function shows a particular user.
    """
    #return a particular user
    print("Retrieve user #{}".format(user_id))
    result = user_get(user_id)
    return Response(json.dumps(result), mimetype="application/json")

@APP.route("/api/user", methods=["POST"])
def user_add():
    """
    This function creates a new user.
    """
    #execute and return result
    json_data = get_data(request.data)
    print("Create user #{}".format(json_data["item"]["name"]))
    result = user_create(
        json_data["item"]["id"], json_data["item"]["name"],
        json_data["item"]["mail"])
    return Response(return_result(result), mimetype="application/json")

@APP.route("/api/user/<int:user_id>", methods=["PUT"])
def user_change(user_id):
    """
    This function updates an existing user.

    :param user_id: user ID
    :type user_id: int
    """
    #execute and return result
    print("Update user #{}".format(user_id))
    json_data = get_data(request.data)
    result = user_update(
        user_id, json_data["item"]["id"],
        json_data["item"]["name"], json_data["item"]["mail"]
    )
    return Response(return_result(result), mimetype="application/json")

@APP.route("/api/user/<int:user_id>", methods=["DELETE"])
def user_delete(user_id):
    """
    This function removes an user.

    :param user_id: user ID
    :type user_id: int
    """
    print("Delete user #{}".format(user_id))
    result = user_remove(user_id)
    return Response(return_result(result), mimetype="application/json")

if __name__ == "__main__":
    global DB_CONN
    global DB_CUR

    #register atexit
    atexit.register(shutdown)
    #start database
    DB_CONN = sqlite3.connect("users.db")
    DB_CUR = DB_CONN.cursor()
    #enable if you also like to live dangerously
    #APP.run(debug=False, host="0.0.0.0")
    APP.run(debug=False)
