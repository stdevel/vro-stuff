#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A script that deploys the demo database.
"""
import sqlite3

#populate demo database
DB_CONN = sqlite3.connect("passwords.db")
DB_CUR = DB_CONN.cursor()
DB_CUR.execute('''CREATE TABLE passwords(
pass_id INTEGER PRIMARY KEY AUTOINCREMENT,
pass_name TEXT NOT NULL,
pass_desc TEXT NOT NULL,
pass_hostname TEXT NOT NULL,
pass_username TEXT NOT NULL,
pass_password TEXT NOT NULL);''')
DB_CUR.execute('''INSERT INTO passwords (pass_name, pass_desc, pass_hostname,
    pass_username, pass_password) VALUES ('demo1', 'Demo password entry 1',
    'localhost', 'admin', 'admin');''')
DB_CUR.execute('''INSERT INTO passwords (pass_name, pass_desc, pass_hostname,
    pass_username, pass_password) VALUES ('demo2', 'Demo password entry 2',
    'localhost', 'pinkepank', 'simonegiertz');''')
DB_CONN.commit()
DB_CONN.close()
