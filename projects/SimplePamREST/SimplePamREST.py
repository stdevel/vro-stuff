#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A simple Flask-based PAM application that might be used for demo purposes.
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
def pass_create(pass_id, pass_name, pass_desc, pass_hostname,
                pass_username, pass_password):
    """
    This function creates a password.

    :param pass_id: password ID
    :type pass_id: int
    :param pass_name: password name
    :type pass_name: str
    :param pass_desc: password description
    :type pass_desc: str
    :param pass_hostname: hostnamne
    :type pass_hostname: str
    :param pass_username: username
    :type pass_username: str
    :param pass_password: password
    :type pass_password: str
    """
    global DB_CONN
    global DB_CUR

    try:
        DB_CUR.execute(
            """INSERT INTO passwords (pass_id, pass_name, pass_desc,
            pass_hostname, pass_username, pass_password) VALUES (?, ?, ?,
            ?, ?, ?)""",
            (
                pass_id, pass_name, pass_desc, pass_hostname, pass_username,
                pass_password
            )
        )
        DB_CONN.commit()
        print(
            "Added password with name={},desc={},hostname={},username={},"
            "password=xxx".format(
                pass_name, pass_desc, pass_hostname, pass_username
            )
            )
        return True
    except Exception as err:
        print(
            "Unable to create user with name={},desc={},hostname={},"
            "username={}: {}".format(
                pass_name, pass_desc, pass_hostname, pass_username, err
            )
        )
        return False

def pass_update(pass_id, pass_newid, pass_name, pass_desc, pass_hostname,
                pass_username, pass_password):
    """
    This function updates an user.

    :param pass_id: password ID
    :type pass_id: int
    :param pass_name: password name
    :type pass_name: str
    :param pass_desc: password description
    :type pass_desc: str
    :param pass_hostname: hostnamne
    :type pass_hostname: str
    :param pass_username: username
    :type pass_username: str
    :param pass_password: password
    :type pass_password: str
    """
    global DB_CONN
    global DB_CUR

    try:
        DB_CUR.execute(
            """UPDATE passwords SET pass_id=?, pass_name=?, pass_desc=?,
            pass_hostname=?, pass_username=?, pass_password=?
            WHERE pass_id=?""",
            (
                pass_newid, pass_name, pass_desc, pass_hostname, pass_username,
                pass_password, pass_id
            )
        )
        DB_CONN.commit()
        print(
            "Updated password #{} with id={},name={},desc={},hostname={},"
            "username={},password=xxx".format(
                pass_id, pass_newid, pass_name, pass_desc,
                pass_hostname, pass_username
            )
        )
        return True
    except Exception as err:
        print(
            "Unable to update password #{} with id={},name={},desc={},"
            "hostname={},username={}: {}".format(
                pass_id, pass_newid, pass_name, pass_desc,
                pass_hostname, pass_username, err
            )
        )
        return False

def pass_remove(pass_id):
    """
    This function removes a password.

    :param pass_id: password ID
    :type pass_id: int
    """
    global DB_CONN
    global DB_CUR

    print("About to remove password #{}".format(pass_id))
    try:
        DB_CUR.execute(
            "DELETE FROM passwords WHERE pass_id=?",
            (pass_id,)
        )
        DB_CONN.commit()
        #check whether a password was removed
        if DB_CUR.rowcount > 0:
            print("Removed password #{}".format(pass_id))
            return True
        return False
    except Exception as err:
        print("Unable to remove password #{}: {}".format(
            pass_id, err
        ))
        return False

def pass_get(pass_id):
    """
    This function retrieves a password's information.

    :param pass_id: password ID
    :type pass_id: int
    """
    global DB_CUR

    #execute database query
    if pass_id > 0:
        #return all passwords
        DB_CUR.execute(
            "SELECT * FROM passwords WHERE pass_id=?;",
            (pass_id,)
        )
    else:
        #return one particular password
        DB_CUR.execute("SELECT * FROM passwords;")

    #prepare result
    json = {}
    results = []
    temp = {}
    #get _all_ the information
    for row in DB_CUR:
        temp[row[0]] = {}
        temp[row[0]]["id"] = row[0]
        temp[row[0]]["name"] = row[1]
        temp[row[0]]["desc"] = row[2]
        temp[row[0]]["hostname"] = row[3]
        temp[row[0]]["username"] = row[4]
        temp[row[0]]["password"] = row[5]
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

@APP.route("/password/create", methods=["GET", "POST"])
def form_create():
    """
    This function presents the form to create passwords and returns the result.
    """
    if request.method == "POST":
        #create password
        if pass_create(
                request.form["id"], request.form["name"], request.form["desc"],
                request.form["hostname"], request.form["username"],
                request.form["password"]
            ):
            return "Password created!"
        return "Password could not be created!"
    else:
        #show form
        return render_template("create.html")

@APP.route("/password/", methods=["GET"])
def form_users():
    """
    This function lists all passwords.
    """
    #get _all_ the users
    passwords = pass_get(0)
    #render users in HTML template
    return render_template("passwords.html", result=passwords)

@APP.route("/password/<int:pass_id>", methods=["GET"])
def form_user(pass_id):
    """
    This function displays a particular password.

    :param pass_id: password ID
    :type pass_id: int
    """
    #display a particular password
    result = pass_get(pass_id)["results"][0]
    return render_template("pass.html", passwd=result)

@APP.route("/password/delete/<int:pass_id>", methods=["GET"])
def from_delete(pass_id):
    """
    This function deletes a particular password.

    :param pass_id: password ID
    :type pass_id: int
    """
    #try to delete password
    if pass_delete(pass_id):
        return "Password deleted!"
    return "Password could not be deleted!"

@APP.route("/password/edit/<int:pass_id>", methods=["GET", "POST"])
def form_edit(pass_id):
    """
    This function presents the form to edit passwordsw and returns form
    data to the API.

    :param pass_id: password ID
    :type pass_id: int
    """
    if request.method == "POST":
        #edit password
        if pass_update(
                pass_id, request.form["id"], request.form["name"],
                request.form["desc"], request.form["hostname"],
                request.form["username"], request.form["password"]
            ):
            return "Password edited!"
        return "Password could not be edited!"
    else:
        #show form, preselect values
        #result = pass_get(pass_id)["results"][0]
        try:
            result = pass_get(pass_id)["results"][0]
            return render_template("edit.html", passwd=result)
        except IndexError:
            return render_template("nonexist.html")



#FLASK API FUNCTIONS
@APP.route("/api/password/<int:pass_id>", methods=["GET"])
def pass_show(pass_id):
    """
    This function shows a particular password.
    """
    #return a particular password
    print("Retrieve password #{}".format(pass_id))
    result = pass_get(pass_id)
    return Response(json.dumps(result), mimetype="application/json")

@APP.route("/api/password", methods=["POST"])
def pass_add():
    """
    This function creates a new password.
    """
    #execute and return result
    json_data = get_data(request.data)
    print("Create password #{}".format(json_data["item"]["name"]))
    result = pass_create(
        json_data["item"]["id"], json_data["item"]["name"],
        json_data["item"]["desc"], json_data["item"]["hostname"],
        json_data["item"]["username"], json_data["item"]["password"])
    return Response(return_result(result), mimetype="application/json")

@APP.route("/api/password/<int:pass_id>", methods=["PUT"])
def pass_change(pass_id):
    """
    This function updates a existing password.

    :param pass_id: password ID
    :type pass_id: int
    """
    #execute and return result
    print("Update password #{}".format(pass_id))
    json_data = get_data(request.data)
    result = pass_update(
        pass_id, json_data["item"]["id"],
        json_data["item"]["name"], json_data["item"]["desc"],
        json_data["item"]["hostname"], json_data["item"]["username"],
        json_data["item"]["password"]
    )
    return Response(return_result(result), mimetype="application/json")

@APP.route("/api/password/<int:pass_id>", methods=["DELETE"])
def pass_delete(pass_id):
    """
    This function removes a password.

    :param pass_id: password ID
    :type pass_id: int
    """
    print("Delete password #{}".format(pass_id))
    result = pass_remove(pass_id)
    return Response(return_result(result), mimetype="application/json")

if __name__ == "__main__":
    global DB_CONN
    global DB_CUR

    #register atexit
    atexit.register(shutdown)
    #start database
    DB_CONN = sqlite3.connect("passwords.db")
    DB_CUR = DB_CONN.cursor()
    #enable if you also like to live dangerously
    #app.run(debug=False, host="0.0.0.0")
    APP.run(debug=False)
