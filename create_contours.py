#!/usr/bin/env python

import os

dgmFile = "334245636_dgm1.tif"
intervall = 10
name = "contour"

os.system("gdal_contour -inodata -snodata -32768 -a ele "  + dgmFile + " " + name + ".sqlite -i " + str(intervall))