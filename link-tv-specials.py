#!/usr/bin/env python3.7

from IO.YAML.object_to_yaml import write_python_dictionary_object_to_yaml_file
from class_objects import Movies
from movies.movies_parser import parse_all_movies_from_yaml
import sqlite3


if __name__ == "__main__":
	connection = sqlite3.connect("company.db")
	
	cursor = connection.cursor()
	
	# delete
	# cursor.execute("""DROP TABLE employee;""")
	
	sql_command = """
	CREATE TABLE movies (
	staff_number INTEGER PRIMARY KEY,
	fname VARCHAR(20),
	lname VARCHAR(30),
	gender CHAR(1),
	joining DATE,
	birth_date DATE);"""
	
	cursor.execute(sql_command)
	
	sql_command = """INSERT INTO movies (staff_number, fname, lname, gender, birth_date)
	    VALUES (NULL, "William", "Shakespeare", "m", "1961-10-25");"""
	cursor.execute(sql_command)
	
	sql_command = """INSERT INTO movies (staff_number, fname, lname, gender, birth_date)
	    VALUES (NULL, "Frank", "Schiller", "m", "1955-08-17");"""
	cursor.execute(sql_command)
	
	# never forget this, if you want the changes to be saved:
	connection.commit()
	
	connection.close()
	exit(-1)
	full_movie_database = Movies()
	parse_all_movies_from_yaml(full_movie_database)
	write_python_dictionary_object_to_yaml_file(full_movie_database)
