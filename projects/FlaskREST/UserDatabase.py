#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3

conn = None
cursor = None

def ___init___(filename):
    """
    This constructor opens an user database.

    :param filename: database filename
    :type filename: str
    """
    global conn
    global cursor

    conn = sqlite3.connect(filename)
    cursor = conn.cursor()
