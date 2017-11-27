#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

"""Test Units
"""
from bob.db.uvad.config import database as db
import os
import nose


def assert_nfiles(files, total, nbonafide, nattack):
    len_files = len(files)
    assert len_files == total, len_files
    len_bonafide = len([f for f in files if f.attack_type is None])
    len_attack = len_files - len_bonafide
    assert len_bonafide == nbonafide, len_bonafide
    assert len_attack == nattack, len_attack


def test_database():
    protocol = 'experiment_1'
    db.protocol = protocol
    assert len(db.all_files(('train', 'dev'))[0])
    assert len(db.all_files(('train', 'dev'))[1])
    assert_nfiles(db.objects(protocol=protocol), 5244,
                  404, 4840)
    assert_nfiles(db.objects(protocol=protocol,
                             groups='train'), 2768, 344, 2424)
    assert_nfiles(db.objects(protocol=protocol, groups='dev'), 2476, 60, 2416)


def test_frames():
    protocol = 'experiment_1'
    db.protocol = protocol
    db.replace_directories(os.path.expanduser('~/.bob_bio_databases.txt'))
    if db.original_directory == '[UVAD_DIRECTORY]':
        raise nose.SkipTest(
            "Please update '[UVAD_DIRECTORY]' in your "
            "'~/.bob_bio_databases.txt' to point to the directory where the "
            "database's raw data are. This way we can test more features of "
            "the database interface.")
    padfile = db.all_files(('train', 'dev'))[0][0]
    assert db.number_of_frames(padfile) == 270, db.number_of_frames(padfile)
