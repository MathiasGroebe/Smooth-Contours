#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import string
import random
import sys
import getopt

def randomString(): # Calculate a random string
    length = 6
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def smoothTerrain(inputTerrain, kernelSize):

    inputDEM = inputTerrain
    prefix = randomString()
    smooth = kernelSize

    os.system("gdal_translate -ot Float32 -a_nodata -32768 "  + inputDEM + " " + prefix + "_dem.tif")

    # Calculate TPI
    print("Calculate TPI...")
    os.system("gdaldem TPI " + inputDEM + " " + prefix + "_dem_tpi.tif")

    # Build VRT for soft smoothed DEM
    print("Smooth DEM...")
    os.system("gdalbuildvrt " + prefix + "_dem_blur_3x3.vrt " + prefix + "_dem.tif")

    file = open(prefix + "_dem_blur_3x3.vrt", "rt")
    data = file.read()
    data = data.replace("ComplexSource", "KernelFilteredSource")
    data = data.replace("<NODATA>-32768</NODATA>", '<NODATA>-32768</NODATA><Kernel normalized="1"><Size>3</Size><Coefs>0.077847 0.123317 0.077847 0.123317 0.195346 0.123317 0.077847 0.123317 0.077847</Coefs></Kernel>')
    file.close()

    file = open(prefix + "_dem_blur_3x3.vrt", "wt")
    file.write(data)
    file.close()

    # Build VRT for smoothed DEM
    os.system("gdalbuildvrt " + prefix + "_dem_blur_5x5.vrt " + prefix + "_dem.tif")

    file = open(prefix + "_dem_blur_5x5.vrt", "rt")
    data = file.read()
    data = data.replace("ComplexSource", "KernelFilteredSource")
    data = data.replace("<NODATA>-32768</NODATA>", '<NODATA>-32768</NODATA><Kernel normalized="1"><Size>5</Size><Coefs>0.003765 0.015019 0.023792 0.015019 0.003765 0.015019 0.059912 0.094907 0.059912 0.015019 0.023792 0.094907 0.150342 0.094907 0.023792 0.015019 0.059912 0.094907 0.059912 0.015019 0.003765 0.015019 0.023792 0.015019 0.003765</Coefs></Kernel>')
    file.close()

    file = open(prefix + "_dem_blur_5x5.vrt", "wt")
    file.write(data)
    file.close()

    # Build VRT for more smoothed DEM
    os.system("gdalbuildvrt " + prefix + "_dem_blur_7x7.vrt " + prefix + "_dem.tif")

    file = open(prefix + "_dem_blur_7x7.vrt", "rt")
    data = file.read()
    data = data.replace("ComplexSource", "KernelFilteredSource")
    data = data.replace("<NODATA>-32768</NODATA>", '<NODATA>-32768</NODATA><Kernel normalized="1"><Size>7</Size><Coefs>0.000036 0.000363 0.001446 0.002291 0.001446 0.000363 0.000036 0.000363 0.003676 0.014662 0.023226 0.014662 0.003676 0.000363 0.001446 0.014662 0.058488 0.092651 0.058488 0.014662 0.001446 0.002291 0.023226 0.092651 0.146768 0.092651 0.023226 0.002291 0.001446 0.014662 0.058488 0.092651 0.058488 0.014662 0.001446 0.000363 0.003676 0.014662 0.023226 0.014662 0.003676 0.000363 0.000036 0.000363 0.001446 0.002291 0.001446 0.000363 0.000036</Coefs></Kernel>')
    file.close()

    file = open(prefix + "_dem_blur_7x7.vrt", "wt")
    file.write(data)
    file.close()

    # Build VRT for more stronger smoothed DEM
    os.system("gdalbuildvrt " + prefix + "_dem_blur_9x9.vrt " + prefix + "_dem.tif")

    file = open(prefix + "_dem_blur_9x9.vrt", "rt")
    data = file.read()
    data = data.replace("ComplexSource", "KernelFilteredSource")
    data = data.replace("<NODATA>-32768</NODATA>", '<NODATA>-32768</NODATA><Kernel normalized="1"><Size>9</Size><Coefs>0 0.000001 0.000014 0.000055 0.000088 0.000055 0.000014 0.000001 0 0.000001 0.000036 0.000362 0.001445 0.002289 0.001445 0.000362 0.000036 0.000001 0.000014 0.000362 0.003672 0.014648 0.023205 0.014648 0.003672 0.000362 0.000014 0.000055 0.001445 0.014648 0.058434 0.092566 0.058434 0.014648 0.001445 0.000055 0.000088 0.002289 0.023205 0.092566 0.146634 0.092566 0.023205 0.002289 0.000088 0.000055 0.001445 0.014648 0.058434 0.092566 0.058434 0.014648 0.001445 0.000055 0.000014 0.000362 0.003672 0.014648 0.023205 0.014648 0.003672 0.000362 0.000014 0.000001 0.000036 0.000362 0.001445 0.002289 0.001445 0.000362 0.000036 0.000001 0 0.000001 0.000014 0.000055 0.000088 0.000055 0.000014 0.000001 0</Coefs></Kernel>')
    file.close()

    file = open(prefix + "_dem_blur_9x9.vrt", "wt")
    file.write(data)
    file.close()

    # Build VRT for strong smoothed DEM
    os.system("gdalbuildvrt " + prefix + "_dem_blur_13x13.vrt " + prefix + "_dem.tif")

    file = open(prefix + "_dem_blur_13x13.vrt", "rt")
    data = file.read()
    data = data.replace("ComplexSource", "KernelFilteredSource")
    data = data.replace("<NODATA>-32768</NODATA>", '<NODATA>-32768</NODATA><Kernel normalized="1"><Size>13</Size><Coefs>0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.000001 0.000001 0.000001 0 0 0 0 0 0 0 0 0.000001 0.000014 0.000055 0.000088 0.000055 0.000014 0.000001 0 0 0 0 0 0.000001 0.000036 0.000362 0.001445 0.002289 0.001445 0.000362 0.000036 0.000001 0 0 0 0 0.000014 0.000362 0.003672 0.014648 0.023204 0.014648 0.003672 0.000362 0.000014 0 0 0 0.000001 0.000055 0.001445 0.014648 0.058433 0.092564 0.058433 0.014648 0.001445 0.000055 0.000001 0 0 0.000001 0.000088 0.002289 0.023204 0.092564 0.146632 0.092564 0.023204 0.002289 0.000088 0.000001 0 0 0.000001 0.000055 0.001445 0.014648 0.058433 0.092564 0.058433 0.014648 0.001445 0.000055 0.000001 0 0 0 0.000014 0.000362 0.003672 0.014648 0.023204 0.014648 0.003672 0.000362 0.000014 0 0 0 0 0.000001 0.000036 0.000362 0.001445 0.002289 0.001445 0.000362 0.000036 0.000001 0 0 0 0 0 0.000001 0.000014 0.000055 0.000088 0.000055 0.000014 0.000001 0 0 0 0 0 0 0 0 0.000001 0.000001 0.000001 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0</Coefs></Kernel>')
    file.close()

    file = open(prefix + "_dem_blur_13x13.vrt", "wt")
    file.write(data)
    file.close()

    print("Reclassify and smooth TPI...")
    # Reclassify TPI
    os.system('gdal_calc.py -A ' + prefix + '_dem_tpi.tif --outfile=' + prefix + '_tpi_pos.tif --NoDataValue=-32768 --calc="((-1)*A*(A<0))+(A*(A>=0))"')
    # Build VRT for smooth TPI
    os.system("gdalbuildvrt " + prefix + "_tpi_blur_3x3.vrt " + prefix + "_tpi_pos.tif")

    file = open(prefix + "_tpi_blur_3x3.vrt", "rt")
    data = file.read()
    data = data.replace("ComplexSource", "KernelFilteredSource")
    data = data.replace("<NODATA>-32768</NODATA>", '<NODATA>-32768</NODATA><Kernel normalized="1"><Size>3</Size><Coefs>0.077847 0.123317 0.077847 0.123317 0.195346 0.123317 0.077847 0.123317 0.077847</Coefs></Kernel>')
    file.close()

    file = open(prefix + "_tpi_blur_3x3.vrt", "wt")
    file.write(data)
    file.close()

    info = os.popen("gdalinfo " + prefix + "_tpi_blur_3x3.vrt -hist").read()

    # Normalize smoothed TPI, if no max avaible than just copy file
    try:
        maxValue = re.findall('[0-9]*\.[0-9]*', re.findall('STATISTICS_MAXIMUM=\d*.\d*', info)[0])[0]
        os.system('gdal_calc.py -A ' + prefix + '_tpi_blur_3x3.vrt --outfile=' + prefix + '_tpi_norm.tif --NoDataValue=-32768 --calc="A / ' + maxValue + '"')
    except:
        os.system("gdal_translate " + prefix + "_tpi_blur_3x3.vrt " + prefix + "_tpi_norm.tif")

    # Combine it together
    print("Build better DEM for contour lines...")

    print(str(smooth))


    if (smooth == 13):
        os.system('gdal_calc.py -A ' + prefix + '_tpi_norm.tif -B ' + prefix + '_dem_blur_3x3.vrt -C ' + prefix + '_dem_blur_13x13.vrt --outfile="smooth_' + inputDEM + '" --overwrite --calc="A*B+(1-A)*C"')
    if (smooth == 7):
        os.system('gdal_calc.py -A ' + prefix + '_tpi_norm.tif -B ' + prefix + '_dem_blur_3x3.vrt -C ' + prefix + '_dem_blur_7x7.vrt --outfile="smooth_' + inputDEM + '" --overwrite --calc="A*B+(1-A)*C"')   
    if (smooth == 5):
        os.system('gdal_calc.py -A ' + prefix + '_tpi_norm.tif -B ' + prefix + '_dem_blur_3x3.vrt -C ' + prefix + '_dem_blur_5x5.vrt --outfile="smooth_' + inputDEM + '" --overwrite --calc="A*B+(1-A)*C"')    
    if (smooth == 3):
        os.system('gdal_calc.py -A ' + prefix + '_tpi_norm.tif -B ' + prefix + '_dem_blur_3x3.vrt -C ' + prefix + '_dem_blur_3x3.vrt --outfile="smooth_' + inputDEM + '" --overwrite --calc="A*B+(1-A)*C"')   
    else:
        os.system('gdal_calc.py -A ' + prefix + '_tpi_norm.tif -B ' + prefix + '_dem_blur_3x3.vrt -C ' + prefix + '_dem_blur_9x9.vrt --outfile="smooth_' + inputDEM + '" --overwrite --calc="A*B+(1-A)*C"')

    # Clean up
    os.remove(prefix + "_dem.tif")
    os.remove(prefix + "_dem_tpi.tif")
    os.remove(prefix + "_dem_blur_3x3.vrt")
    os.remove(prefix + "_dem_blur_5x5.vrt")
    os.remove(prefix + "_dem_blur_7x7.vrt")
    os.remove(prefix + "_dem_blur_9x9.vrt")
    os.remove(prefix + "_dem_blur_13x13.vrt")
    os.remove(prefix + "_tpi_pos.tif")
    os.remove(prefix + "_tpi_pos.tif.aux.xml")
    os.remove(prefix + "_tpi_blur_3x3.vrt")
    os.remove(prefix + "_tpi_norm.tif")

    return("smooth_" + inputDEM)

def main(argv):
    inputDEM = ''
    outputFile = ''
    interval = ''
    pixelSize = ''
    gaussainBlur = ''

    tmp_file = "resample_dem.tif"
    overwrite = True

    try:
        opts, args = getopt.getopt(argv, "", ["help", "inputDEM=", "outputFile=", "intervall=", "pixelSize=", "gaussainBlur="]) 
    except getopt.GetoptError:
        print("Please look use create_contours.py --help to get more information how to use the script. ")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("--help"):
            print("Create smooth contours with the help of GDAL. Usage:")
            print("\tcreate_contour.py --inputDEM=DEMfile.tif --outputFile=contours.geoJSON --intervall=5 --pixelSize=2")
            print("Algorithm after: P. Kettunen, C. Koski, and J. Oksanen, 'A design of contour generation for topographic maps with adaptive DEM smoothing' International Journal of Cartography, vol. 3, no. 1, pp. 19–30, Jun. 2017.")
            print("Parameters:")
            print("\t--inputDEM=(rasterFilename)* put here your DEM in any GDAL readable format.")
            print("\t--outputFile=(vectorFilename)* write the name of the outputfile for the contours. The format is guessed form the extention")
            print("\t--intervall=(float)* intervall between the contour lines.")
            print("\t--pixelSize=(float)* pixel size of the DEM, or a greater number. Used for reampling and should correspond with the aimed map scale")
            print("\t--gaussainBlur={3, 5, 7, 9, 13} kernel size for smoothing flat areas. Default 9.")
            print("\t--help print this hopefully hepfully text.")
            print("\t*necessary for execution.")
            print("Mathias Gröbe 2020")
            sys.exit(0)
        elif opt in ("--inputDEM"):
            inputDEM = arg #dem_file.tif
        elif opt in ("--outputFile"):
            outputFile = arg #contour.sqlite
        elif opt in ("--intervall"): 
            interval = arg #5
        elif opt in ("--pixelSize"):
            pixelSize = arg #10
        elif opt in ("--gaussainBlur"):
            gaussainBlur = arg #{3, 9, 13}
    
    if (inputDEM != '') & (outputFile != '') & (interval != '') & (pixelSize != ''):

        # Resample
        os.system("gdal_translate " + inputDEM + " " + tmp_file + " -tr "  + str(pixelSize) + " " + str(pixelSize) + " -r cubic")

        # Smooth terrain
        smooth_dem = smoothTerrain(tmp_file, gaussainBlur)

        # Create contour lines file
        print("Create contour lines...")

        if(overwrite):
            try:
                os.remove(outputFile)
                print("Overwrite old file.")
                os.system("gdal_contour -inodata -snodata -32768 -a ele "  + smooth_dem + " " + outputFile + " -i " + str(interval))
            except:
                if os.path.isfile(outputFile):
                    print("Can not delete old file! Is it open in a GIS?")
                else:
                    print("Create " + outputFile + ".")
                    os.system("gdal_contour -inodata -snodata -32768 -a ele "  + smooth_dem + " " + outputFile + " -i " + str(interval))

        # Clean up
        os.remove(tmp_file)
        os.remove(smooth_dem)

    else:
        print("Sorry, missing some information. Please see help.")
        print("create_contour.py --help")
        sys.exit(2)

if __name__ == "__main__":
   main(sys.argv[1:])
