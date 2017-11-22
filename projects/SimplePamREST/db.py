#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3

#populate demo database
conn = sqlite3.connect("passwords.db")
c = conn.cursor()
c.execute('''CREATE TABLE passwords(
pass_id INTEGER PRIMARY KEY AUTOINCREMENT,
pass_name TEXT NOT NULL,
pass_desc TEXT NOT NULL,
pass_hostname TEXT NOT NULL,
pass_username TEXT NOT NULL,
pass_password TEXT NOT NULL);''')
c.execute('''INSERT INTO passwords (pass_name, pass_desc, pass_hostname, pass_username, pass_password)
    VALUES ('demo1', 'Demo password entry 1', 'localhost', 'admin', 'admin');''')
c.execute('''INSERT INTO passwords (pass_name, pass_desc, pass_hostname, pass_username, pass_password)
    VALUES ('demo2', 'Demo password entry 2', 'localhost', 'pinkepank', 'simonegiertz');''')
conn.commit()
conn.close()
