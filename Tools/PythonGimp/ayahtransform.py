#!/usr/bin/env python

#   Python-Fu-Photofy - Makes the selected layer look like a printed photo
#
#   Copyright (C) 2011  Steven Occhipinti <StevenOcchipinti.com>
#   Creative Commons - Attribution 3.0 Unported (CC BY 3.0)
#   http://creativecommons.org/licenses/by/3.0/
#
#   This is my first attempt at a python-fu gimp plugin, so there are
#   a few hacks that I didn't know how to get around due to lack of
#   understanding. Also, this plugin is heavily commented so I can use
#   this an example for future attempts. A few note-worthy points are to
#   ensure the file is in ~/.gimp-2.6/plug-ins/ (with your particular
#   version of course) and is executable.

from gimpfu import *
from gimpayahbounds import *

# ==============================================================================
# This puts the filter in the menu :)

register(
    "python-fu-ayahbox",
    "This will allow boxes to be drawn around the ayahs of the page",
    "The main image editor for quran pages",
    "Mohammad Saleh",
    "Blackstone eIT",
    "2017",
    "Ayahbox...",
    "*",
    [
        (PF_IMAGE, "image", "Input image", None),
        (PF_DRAWABLE, "drawable", "Input drawable", None),
        (PF_STRING, "data_file_name", "Data Input Filename", ""),
        (PF_FLOAT,    "scale", "Scale of whole boxes", 1.0),
        (PF_INT, "x_offset_odd", "Move odd boxes by x steps", 0),
        (PF_INT, "y_offset_odd", "Move odd boxes by y steps", 0),
        (PF_INT, "x_offset_even", "Move even boxes by x steps", 0),
        (PF_INT, "y_offset_even", "Move even boxes by y steps", 0),
    ],
    [],
    ayah_bounds,
    menu="<Image>/Filters/AyahBounds",
)

main()
