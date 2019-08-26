#!/usr/bin/env python3.7

from IO.YAML.object_to_yaml import write_python_dictionary_object_to_yaml_file
from class_objects import Movies
from movies.movies_parser import parse_all_movies_from_yaml
import sqlite3


if __name__ == "__main__":
	connection = sqlite3.connect("config_files/movies_collection.db")
	
	cursor = connection.cursor()
	
	# delete
	cursor.execute("""DROP TABLE movies;""")
	
	sql_command = """
	CREATE TABLE movies (
	movie_title VARCHAR(50) PRIMARY KEY);"""
	cursor.execute(sql_command)
	
	sql_command = """INSERT INTO movies (movie_title) VALUES (NULL);"""
	cursor.execute(sql_command)
	# never forget this, if you want the changes to be saved:
	connection.commit()
	
	connection.close()
	exit(-1)
	full_movie_database = Movies()
	parse_all_movies_from_yaml(full_movie_database)
	write_python_dictionary_object_to_yaml_file(full_movie_database)
