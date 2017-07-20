#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3

#populate demo database
conn = sqlite3.connect("users.db")
c = conn.cursor()
c.execute('''CREATE TABLE users(
user_id INTEGER PRIMARY KEY AUTOINCREMENT,
user_name TEXT NOT NULL,
user_mail TEXT NOT NULL);''')
c.execute('''INSERT INTO users (user_name, user_mail)
    VALUES ('Simone Giertz', 'giertz@shittyrobots.loc');''')
c.execute('''INSERT INTO users (user_name, user_mail)
    VALUES ('Paula Pinkepank', 'paula@pinkepa.nk');''')
conn.commit()
conn.close()
