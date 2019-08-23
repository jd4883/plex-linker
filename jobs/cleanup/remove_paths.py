#!/usr/bin/env python3
from shutil import rmtree


def remove_directory_and_contents(path):
	rmtree(path)


def remove_blacklsited_items(path):
	if path is 'lost+found':
		remove_directory_and_contents(path)
