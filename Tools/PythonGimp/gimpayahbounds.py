
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
from re import *
from qurandatatransform import *

def ayah_bounds(image, drawable, data_file_name,
                scale,
                x_offset_odd, y_offset_odd,
                x_offset_even, y_offset_even
                ):
    # Separate contectual changes (brush, colors, etc.) from the user
    gimp.context_push()
    # Allow all these changes to appear as 1 atomic action (1 undo)
    image.undo_group_start()

    # These commands were used while testing interactively
    # image = gimp.image_list()[0]
    # layer = pdb.gimp_image_get_active_layer(image)

    page = int(findall(r'\d+', image.name)[0])

    # layer = image.active_layer
    layer = drawable

    # Capture the transformation dictionary from the dialog
    transform_dict = {
        ALL: [AyahBoxTransform.Scale(scale=scale)],
        ODD: [AyahBoxTransform.Move(x_offset=x_offset_odd, y_offset=y_offset_odd)],
        EVEN: [AyahBoxTransform.Move(x_offset=x_offset_even, y_offset=y_offset_even)],
    }

    # pass the params to get the quran_file object
    quran_trans = QuranDataTransform(quran_data_file_name=data_file_name,
                                     transform_dict=transform_dict)
    quran_trans.parse_quran_data()

    # Draw the quran file strokes for the current page
    for ayahbox in quran_trans.quran_file.pages[page]:
        strokes = []
        strokes.extend(ayahbox.upper_left)
        strokes.extend(ayahbox.upper_right)
        strokes.extend(ayahbox.lower_right)
        strokes.extend(ayahbox.lower_left)
        strokes.extend(ayahbox.upper_left)
        pdb.gimp_pencil(layer, len(strokes), strokes)

    # Leave the user in the same context they were in before
    image.undo_group_end()
    # Return the user to the context they were in before
    gimp.context_pop()
