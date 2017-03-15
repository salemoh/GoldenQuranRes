#!/usr/bin/env python

import xml.etree.ElementTree as et
import re
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import select, func
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from ayahbox import *
from ayahboxtransform import *


class OldDB(object):
    """
    Used to convert an old DB to new format
    """

    def __init__(self, db_name=None, new_db_name=None):
        """
        Init the DB to convert old DB to new format
        :param db_name: DB based on old format
        :param new_db_name: DB updated to new format
        """
        # DB file name and DB persistence
        self.db_name = db_name
        self.new_db_name = new_db_name
        self.engine = None
        self.session = None
        self.connection = None
        self.new_engine = None
        self.new_session = None
        self.new_connection = None

        # Place holder for the glyphs table, and select
        self.glyphs = None
        self.glyphs_select = None

        # In memory of pages
        self.pages = dict()

    def initialize(self):
        # Init the DB
        self.init_db()

    def init_db(self):
        if self.db_name is not None:
            # Init the engine and Session of the DB
            self.engine = create_engine('sqlite:///' + self.db_name, echo=True)
            self.connection = self.engine.connect()
            session = sessionmaker(bind=self.engine)
            self.session = session()

            # Create a selector from glyphs table
            meta = MetaData()
            self.glyphs = Table('glyphs', meta, autoload=True, autoload_with=self.engine)

            # Need to order the query by page, Surah, Ayah, Line
            self.glyphs_select = select([self.glyphs.c.page_number, self.glyphs.c.sura_number,
                                         self.glyphs.c.ayah_number, self.glyphs.c.line_number,
                                         func.min(self.glyphs.c.min_x).label('upper_left_x'),
                                         func.min(self.glyphs.c.min_y).label('upper_left_y'),
                                         func.max(self.glyphs.c.max_x).label('lower_right_x'),
                                         func.max(self.glyphs.c.max_y).label('lower_right_y')]). \
                order_by(self.glyphs.c.page_number, self.glyphs.c.sura_number,
                         self.glyphs.c.ayah_number, self.glyphs.c.line_number). \
                group_by(self.glyphs.c.page_number, self.glyphs.c.sura_number,
                         self.glyphs.c.ayah_number, self.glyphs.c.line_number)

        if self.new_db_name is not None:
            # Init the engine and Session of the DB
            self.new_engine = create_engine('sqlite:///' + self.new_db_name, echo=True)
            new_session = sessionmaker(bind=self.new_engine)
            self.new_session = new_session()

            # Create the meta data of the DB
            Base.metadata.create_all(self.new_engine)

    def parse_db(self, db_persist=False):
        """
        Parse a file into a dictionary of ayahboxes
        :param db_persist:
        :return:
        """

        ayah = 0
        line = 1

        # We loop over row and create a page object and add it to the pages
        for row in self.connection.execute(self.glyphs_select):

            # If ayah changed then reset the line number
            if ayah != row[self.glyphs.c.ayah_number]:
                ayah = row[self.glyphs.c.ayah_number]
                line = 1

            # Calculate the width and height
            width = row['lower_right_x'] - row['upper_left_x']
            height = row['lower_right_y'] - row['upper_left_y']
            x = row['upper_left_x']
            y = row['upper_left_y']

            print 'sura_number=', row[self.glyphs.c.sura_number], '; ayah_number=', row[
                self.glyphs.c.ayah_number], '; line_number=', line, \
                '; page_number=', row[self.glyphs.c.page_number], \
                '; old_line_number=', row[self.glyphs.c.line_number], \
                '; upper_left_x=', row['upper_left_x'], '; upper_left_y=', row['upper_left_y'], \
                '; lower_right_x=', row['lower_right_x'], '; lower_right_y=', row['lower_right_y'], \
                '; x=', x, '; y=', y, \
                '; width=', width, '; height=', height

            # Add a new ayahbox to pages
            ayahbox = AyahBox(page_number=row[self.glyphs.c.page_number],
                              surah=row[self.glyphs.c.sura_number],
                              ayah=row[self.glyphs.c.ayah_number],
                              line=line,
                              x=x, y=y, width=width, height=height)

            # Add to the DB session
            # this assumes the other DB components are initialized
            if db_persist:
                self.new_session.add(ayahbox)

            # Increment line number
            line += 1

        # Commit to the DB
        if db_persist:
            self.new_session.commit()



def db_persist(self):
    # set the number of items to commit
    commit_batch = 10
    counter = 0

    # Loop over the parsed pages
    for ayahbox in self.pages.itervalues():

        # Add the values to the session
        self.session.add(ayahbox)

        # Commit if reached the batch count
        if counter % commit_batch == 0:
            self.session.commit()

        # Increment counter
        counter += 1

    # Commit any last added ayahboxes
    self.session.commit()


if __name__ == '__main__':
    old_db = OldDB(db_name="../../db/KingFahad.db", new_db_name='../../db/KingFahad1.db')
    old_db.initialize()
    old_db.parse_db(db_persist=True)
