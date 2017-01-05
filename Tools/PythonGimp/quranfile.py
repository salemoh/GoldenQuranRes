#!/usr/bin/env python

import xml.etree.ElementTree as et
import re
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from ayahbox import *
from ayahboxtransform import *


class QuranFile(object):
    """
    Used to enumerate a file with quran ayah data and
    """

    def __init__(self, file_name, db_name=None, ayahbox_transform=None):
        """
        Init the Object with DB and transformation
        :param file_name:
        :param db_name:
        """
        # The file to be read
        self.file_name = file_name

        # DB file name and DB persistence
        self.db_name = db_name
        self.engine = None
        self.session = None

        # Transformation for the ayahboxes
        self.ayahbox_transform = ayahbox_transform

        # In memory of pages
        self.pages = dict()

    def initialize(self):

        # Init the DB
        self.init_db()

    def init_db(self):

        if self.db_name is not None:

            # Init the engine and Session of the DB
            self.engine = create_engine('sqlite:///' + self.db_name, echo=True)
            session = sessionmaker(bind=self.engine)
            self.session = session()

            # Create the meta data of the DB
            Base.metadata.create_all(self.engine)

    def parse_file(self, db_persist=False):
        """
        Parse a file into a dictionary of ayahboxes
        :param db_persist:
        :return:
        """
        # Read all pages of the file
        tree = et.parse(self.file_name)
        root = tree.getroot()

        # Iterate and fill the dictionary
        for page in root:

            # init the empty page record
            page_number = int(page.attrib['p'])
            ayah_boxes = []

            # Loop over lines in page
            for line in page:

                # parse the surah, verse, and line number
                surah_ayah_id = line.attrib['id'].split('_')
                surah = int(re.findall(r'\d+', surah_ayah_id[0])[0])
                ayah = int(surah_ayah_id[1])

                # We always have line_number
                line_number = 1
                if len(surah_ayah_id) > 2:
                    line_number = int(surah_ayah_id[2])

                x = int(line.attrib['x'])
                y = int(line.attrib['y'])
                height = int(line.attrib['h'])
                width = int(line.attrib['w'])

                # generate an ayah box from the data
                ayahbox = AyahBox(page_number,
                                  surah,
                                  ayah, line_number,
                                  x, y, height, width)

                # Transform the ayahbox
                if self.ayahbox_transform is not None:
                    self.ayahbox_transform.apply(ayahbox=ayahbox)

                # Add to the DB session
                # this assumes the other DB components are initialized
                if db_persist:
                    self.session.add(ayahbox)

                # build a dictionary of the verse
                ayah_boxes.append(ayahbox)

            # Commit to the DB
            if db_persist:
                self.session.commit()

            # Add the page to the dictionary
            self.pages[page_number] = ayah_boxes

    def db_persist(self):

        # set the number of items to commit
        commit_batch = 10
        counter = 0

        # Loop over the parsed pages
        for ayahbox in self.pages.itervalues():

            # Add the values to the session
            self.session.add(ayahbox)

            # Commit if reached the batch count
            if counter%commit_batch == 0:
                self.session.commit()

            # Increment counter
            counter += 1

        # Commit any last added ayahboxes
        self.session.commit()
