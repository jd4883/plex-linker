#!/usr/bin/env python3.7

import sqlite3



def add_to_db(command):

connection = sqlite3.connect("movies_collection.db")
cursor = connection.cursor()
cursor.execute(command)
connection.commit()

connection.close()