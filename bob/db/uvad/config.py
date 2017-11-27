#!/usr/bin/env python

from bob.db.uvad import Database

uvad_directory = "[UVAD_DIRECTORY]"

database = Database(
    original_directory=uvad_directory,
)
