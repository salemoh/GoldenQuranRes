#!/usr/bin/env python

from quranfile import *
from ayahboxtransform import *

class QuranDataTransform(object):
    """
    A class to transform an XML file of x,y,width,height into a coordinates for
    Ayah's in a Quran image and write to a DB
    """

    def __init__(self, db_file_name=None, quran_data_file_name=None, transform_dict=None):
        """
        Inits an Ayah Transform object
        :param db_file_name: the DB to store the data into
        :param quran_data_file_name: QuranFlash file to read ayah boxes from
        :param transform_dict: Trasnforms to apply to QuranFlash file
        """
        # the DB file name
        self.db_file_name = db_file_name
        self.quran_data_file_name = quran_data_file_name

        if transform_dict is not None:
            self.ayahbox_transform = AyahBoxTransform(transform_dict=transform_dict)
        else:
            self.ayahbox_transform = None

        self.quran_file = QuranFile(file_name=self.quran_data_file_name,
                                    db_name=self.db_file_name,
                                    ayahbox_transform=self.ayahbox_transform)

    def parse_quran_data(self):

        # Open the xml file
        self.quran_file.initialize()
        self.quran_file.parse_file(db_persist=True)

if __name__ == '__main__':

    # region Median1 ayah transform
    medina_transform_dict = {
        ALL: [AyahBoxTransform.Scale(scale=1.2)],
        ODD: [AyahBoxTransform.Move(x_offset=-70, y_offset=-57)],
        EVEN: [AyahBoxTransform.Move(x_offset=-70, y_offset=-57)]
    }


    medina_ayah_transform = QuranDataTransform(quran_data_file_name='../../data/Medina1.xml',
                                               db_file_name="../../db/Medina1.db",
                                               transform_dict=medina_transform_dict)
    medina_ayah_transform.parse_quran_data()
    print "number of pages parsed in medina: "+str(len(medina_ayah_transform.quran_file.pages))
    # endregion

    # region Warsh ayah transform
    warsh_transform_dict = {
        ALL: [AyahBoxTransform.Scale(scale=1.4)],
        ODD: [AyahBoxTransform.Move(x_offset=-115, y_offset=-100)],
        EVEN: [AyahBoxTransform.Move(x_offset=-67, y_offset=-100)]
    }


    warsh_ayah_transform = QuranDataTransform(quran_data_file_name='../../data/Warsh1.xml',
                                              db_file_name="../../db/Warsh1.db",
                                              transform_dict=warsh_transform_dict)
    warsh_ayah_transform.parse_quran_data()
    print "number of pages parsed warsh: "+str(len(warsh_ayah_transform.quran_file.pages))
    # endregion
