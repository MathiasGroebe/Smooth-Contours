#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import string
import random
import sys
import getopt

import spatialite

def randomString(): # Calculate a random string
    length = 6
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def smoothTerrain(inputTerrain, gaussianBlur, medianBlur):

    inputDEM = inputTerrain
    prefix = randomString()
    method = "gaussain"
    smooth = 9

    if gaussianBlur != '':
        smooth = int(gaussianBlur)
        method = "gaussain"
    if medianBlur != '':
        smooth = int(medianBlur)        
        method = "median"

    os.system("gdal_translate -ot Float32 -a_nodata -32768 "  + inputDEM + " " + prefix + "_dem.tif -q")

    # Calculate TPI
    print("Calculate TPI...")
    os.system("gdaldem TPI " + inputDEM + " " + prefix + "_dem_tpi.tif -q")

    # Build VRT for soft smoothed DEM
    print("Smooth DEM...")
    os.system("gdalbuildvrt " + prefix + "_dem_blur_3x3.vrt " + prefix + "_dem.tif -q")

    file = open(prefix + "_dem_blur_3x3.vrt", "rt")
    data = file.read()
    data = data.replace("ComplexSource", "KernelFilteredSource")
    data = data.replace("<NODATA>-32768</NODATA>", '<NODATA>-32768</NODATA><Kernel normalized="1"><Size>3</Size><Coefs>0.077847 0.123317 0.077847 0.123317 0.195346 0.123317 0.077847 0.123317 0.077847</Coefs></Kernel>')
    file.close()

    file = open(prefix + "_dem_blur_3x3.vrt", "wt")
    file.write(data)
    file.close()

    # Build VRT for soft smoothed DEM with median filter
    os.system("gdalbuildvrt " + prefix + "_dem_median_3x3.vrt " + prefix + "_dem.tif -q")

    file = open(prefix + "_dem_median_3x3.vrt", "rt")
    data = file.read()
    data = data.replace("ComplexSource", "KernelFilteredSource")
    data = data.replace("<NODATA>-32768</NODATA>", '<NODATA>-32768</NODATA><Kernel normalized="1"><Size>3</Size><Coefs>0.11111111 0.11111111 0.11111111 0.11111111 0.11111111 0.11111111 0.11111111 0.11111111 0.11111111</Coefs></Kernel>')
    file.close()

    file = open(prefix + "_dem_median_3x3.vrt", "wt")
    file.write(data)
    file.close()    

    # Build VRT for smoothed DEM
    os.system("gdalbuildvrt " + prefix + "_dem_blur_5x5.vrt " + prefix + "_dem.tif -q")

    file = open(prefix + "_dem_blur_5x5.vrt", "rt")
    data = file.read()
    data = data.replace("ComplexSource", "KernelFilteredSource")
    data = data.replace("<NODATA>-32768</NODATA>", '<NODATA>-32768</NODATA><Kernel normalized="1"><Size>5</Size><Coefs>0.003765 0.015019 0.023792 0.015019 0.003765 0.015019 0.059912 0.094907 0.059912 0.015019 0.023792 0.094907 0.150342 0.094907 0.023792 0.015019 0.059912 0.094907 0.059912 0.015019 0.003765 0.015019 0.023792 0.015019 0.003765</Coefs></Kernel>')
    file.close()

    file = open(prefix + "_dem_blur_5x5.vrt", "wt")
    file.write(data)
    file.close()

    # Build VRT for smoothed DEM (median)
    os.system("gdalbuildvrt " + prefix + "_dem_median_5x5.vrt " + prefix + "_dem.tif -q")

    file = open(prefix + "_dem_median_5x5.vrt", "rt")
    data = file.read()
    data = data.replace("ComplexSource", "KernelFilteredSource")
    data = data.replace("<NODATA>-32768</NODATA>", '<NODATA>-32768</NODATA><Kernel normalized="1"><Size>5</Size><Coefs>0.04 0.04 0.04 0.04 0.04 0.04 0.04 0.04 0.04 0.04 0.04 0.04 0.04 0.04 0.04 0.04 0.04 0.04 0.04 0.04 0.04 0.04 0.04 0.04 0.04 </Coefs></Kernel>')
    file.close()

    file = open(prefix + "_dem_median_5x5.vrt", "wt")
    file.write(data)
    file.close()    

    # Build VRT for more smoothed DEM
    os.system("gdalbuildvrt " + prefix + "_dem_blur_7x7.vrt " + prefix + "_dem.tif -q")

    file = open(prefix + "_dem_blur_7x7.vrt", "rt")
    data = file.read()
    data = data.replace("ComplexSource", "KernelFilteredSource")
    data = data.replace("<NODATA>-32768</NODATA>", '<NODATA>-32768</NODATA><Kernel normalized="1"><Size>7</Size><Coefs>0.000036 0.000363 0.001446 0.002291 0.001446 0.000363 0.000036 0.000363 0.003676 0.014662 0.023226 0.014662 0.003676 0.000363 0.001446 0.014662 0.058488 0.092651 0.058488 0.014662 0.001446 0.002291 0.023226 0.092651 0.146768 0.092651 0.023226 0.002291 0.001446 0.014662 0.058488 0.092651 0.058488 0.014662 0.001446 0.000363 0.003676 0.014662 0.023226 0.014662 0.003676 0.000363 0.000036 0.000363 0.001446 0.002291 0.001446 0.000363 0.000036</Coefs></Kernel>')
    file.close()

    file = open(prefix + "_dem_blur_7x7.vrt", "wt")
    file.write(data)
    file.close()

    # Build VRT for more smoothed DEM (median)
    os.system("gdalbuildvrt " + prefix + "_dem_median_7x7.vrt " + prefix + "_dem.tif -q")

    file = open(prefix + "_dem_median_7x7.vrt", "rt")
    data = file.read()
    data = data.replace("ComplexSource", "KernelFilteredSource")
    data = data.replace("<NODATA>-32768</NODATA>", '<NODATA>-32768</NODATA><Kernel normalized="1"><Size>7</Size><Coefs>0.02 0.02 0.02 0.02 0.02 0.02 0.02 0.02 0.02 0.02 0.02 0.02 0.02 0.02 0.02 0.02 0.02 0.02 0.02 0.02 0.02 0.02 0.02 0.02 0.02 0.02 0.02 0.02 0.02 0.02 0.02 0.02 0.02 0.02 0.02 0.02 0.02 0.02 0.02 0.02 0.02 0.02 0.02 0.02 0.02 0.02 0.02 0.02 0.02 </Coefs></Kernel>')
    file.close()

    file = open(prefix + "_dem_median_7x7.vrt", "wt")
    file.write(data)
    file.close()    

    # Build VRT for more stronger smoothed DEM
    os.system("gdalbuildvrt " + prefix + "_dem_blur_9x9.vrt " + prefix + "_dem.tif -q")

    file = open(prefix + "_dem_blur_9x9.vrt", "rt")
    data = file.read()
    data = data.replace("ComplexSource", "KernelFilteredSource")
    data = data.replace("<NODATA>-32768</NODATA>", '<NODATA>-32768</NODATA><Kernel normalized="1"><Size>9</Size><Coefs>0 0.000001 0.000014 0.000055 0.000088 0.000055 0.000014 0.000001 0 0.000001 0.000036 0.000362 0.001445 0.002289 0.001445 0.000362 0.000036 0.000001 0.000014 0.000362 0.003672 0.014648 0.023205 0.014648 0.003672 0.000362 0.000014 0.000055 0.001445 0.014648 0.058434 0.092566 0.058434 0.014648 0.001445 0.000055 0.000088 0.002289 0.023205 0.092566 0.146634 0.092566 0.023205 0.002289 0.000088 0.000055 0.001445 0.014648 0.058434 0.092566 0.058434 0.014648 0.001445 0.000055 0.000014 0.000362 0.003672 0.014648 0.023205 0.014648 0.003672 0.000362 0.000014 0.000001 0.000036 0.000362 0.001445 0.002289 0.001445 0.000362 0.000036 0.000001 0 0.000001 0.000014 0.000055 0.000088 0.000055 0.000014 0.000001 0</Coefs></Kernel>')
    file.close()

    file = open(prefix + "_dem_blur_9x9.vrt", "wt")
    file.write(data)
    file.close()

    # Build VRT for strong smoothed DEM
    os.system("gdalbuildvrt " + prefix + "_dem_blur_13x13.vrt " + prefix + "_dem.tif -q")

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
    os.system('gdal_calc.py -A ' + prefix + '_dem_tpi.tif --outfile=' + prefix + '_tpi_pos.tif --NoDataValue=-32768 --calc="((-1)*A*(A<0))+(A*(A>=0))" --quiet')
    # Build VRT for smooth TPI
    os.system("gdalbuildvrt " + prefix + "_tpi_blur_3x3.vrt " + prefix + "_tpi_pos.tif -q")

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
        os.system('gdal_calc.py -A ' + prefix + '_tpi_blur_3x3.vrt --outfile=' + prefix + '_tpi_norm.tif --NoDataValue=-32768 --calc="A / ' + maxValue + '" --quiet')
    except:
        os.system("gdal_translate " + prefix + "_tpi_blur_3x3.vrt " + prefix + "_tpi_norm.tif -q")

    # Combine it together
    print("Build better DEM for contour lines...")
    # use gaussian filter
    if (smooth == 13) & (method == "gaussian"):
        print(f"Using gaussian smoothing with value {smooth}...")
        os.system('gdal_calc.py -A ' + prefix + '_tpi_norm.tif -B ' + prefix + '_dem_blur_3x3.vrt -C ' + prefix + '_dem_blur_13x13.vrt --outfile="smooth_' + inputDEM + '" --overwrite --calc="A*B+(1-A)*C" --quiet')
    if (smooth == 9) & (method == "gaussian"):
        print(f"Using gaussian smoothing with value {smooth}...")
        os.system('gdal_calc.py -A ' + prefix + '_tpi_norm.tif -B ' + prefix + '_dem_blur_3x3.vrt -C ' + prefix + '_dem_blur_9x9.vrt --outfile="smooth_' + inputDEM + '" --overwrite --calc="A*B+(1-A)*C" --quiet')    
    if (smooth == 7) & (method == "gaussian"):
        print(f"Using gaussian smoothing with value {smooth}...")
        os.system('gdal_calc.py -A ' + prefix + '_tpi_norm.tif -B ' + prefix + '_dem_blur_3x3.vrt -C ' + prefix + '_dem_blur_7x7.vrt --outfile="smooth_' + inputDEM + '" --overwrite --calc="A*B+(1-A)*C" --quiet')   
    if (smooth == 5) & (method == "gaussian"):
        print(f"Using gaussian smoothing with value {smooth}...")
        os.system('gdal_calc.py -A ' + prefix + '_tpi_norm.tif -B ' + prefix + '_dem_blur_3x3.vrt -C ' + prefix + '_dem_blur_5x5.vrt --outfile="smooth_' + inputDEM + '" --overwrite --calc="A*B+(1-A)*C" --quiet')    
    if (smooth == 3) & (method == "gaussian"):
        print(f"Using gaussian smoothing with value {smooth}...")
        os.system('gdal_calc.py -A ' + prefix + '_tpi_norm.tif -B ' + prefix + '_dem_blur_3x3.vrt -C ' + prefix + '_dem_blur_3x3.vrt --outfile="smooth_' + inputDEM + '" --overwrite --calc="A*B+(1-A)*C" --quiet')   
    # use median filter
    if (smooth == 7) & (method == "median"):
        print(f"Using median smoothing with value {smooth}...")
        os.system('gdal_calc.py -A ' + prefix + '_tpi_norm.tif -B ' + prefix + '_dem_median_3x3.vrt -C ' + prefix + '_dem_median_7x7.vrt --outfile="smooth_' + inputDEM + '" --overwrite --calc="A*B+(1-A)*C" --quiet')   
    if (smooth == 5) & (method == "median"):
        print(f"Using median smoothing with value {smooth}...")
        os.system('gdal_calc.py -A ' + prefix + '_tpi_norm.tif -B ' + prefix + '_dem_median_3x3.vrt -C ' + prefix + '_dem_median_5x5.vrt --outfile="smooth_' + inputDEM + '" --overwrite --calc="A*B+(1-A)*C" --quiet')    
    if (smooth == 3) & (method == "median"):
        print(f"Using median smoothing with value {smooth}...")
        os.system('gdal_calc.py -A ' + prefix + '_tpi_norm.tif -B ' + prefix + '_dem_median_3x3.vrt -C ' + prefix + '_dem_median_3x3.vrt --outfile="smooth_' + inputDEM + '" --overwrite --calc="A*B+(1-A)*C" --quiet')       
    # else ...


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


def createContours(outputFile, smooth_dem, interval, contourBuffer):
    # define variables
    buffer = contourBuffer
    prefix = randomString()
    contoursFile = prefix + "_contour.gpkg"

    if contourBuffer != 0:
        doubleInterval = float(interval) / 2
    else:
        doubleInterval = float(interval) 

    os.system(f"gdal_contour -inodata -a ele  {smooth_dem} {contoursFile} -i {doubleInterval} -q ")
   
    # Calculate length of countour lines
    print("Calculate lenght of contour lines...")
    os.system(f"ogr2ogr {contoursFile} {contoursFile} -update -dialect SQLITE -sql 'ALTER TABLE contour ADD COLUMN line_length float'")
    os.system(f"ogr2ogr {contoursFile} {contoursFile} -update -dialect SQLITE -sql 'UPDATE contour SET line_length = ST_Length(geom)'")
    
    if contourBuffer != 0:
        # Calculate additional contour lines for flatter areas
        print("Calculate additional contour lines for flatter areas...")
        os.system(f"ogr2ogr {contoursFile} {contoursFile} -append -nln 'buffer' -dialect SQLITE -sql 'SELECT id, ele, line_length, ST_Union(ST_Buffer(geom, {buffer} )) as geom FROM contour WHERE (ele % {interval} = 0)'")
        os.system(f"ogr2ogr {contoursFile} {contoursFile} -append -nln 'bbox' -dialect SQLITE -sql 'SELECT ST_Envelope(ST_Union(geom)) as geom FROM contour'")
        os.system(f"ogr2ogr {contoursFile} {contoursFile} -append -nln 'diff' -dialect SQLITE -sql 'SELECT ST_Difference(bbox.geom, buffer.geom) as geom FROM bbox, buffer'")
        os.system(f"ogr2ogr {contoursFile} {contoursFile} -append -nln 'contours_cliped' -nlt PROMOTE_TO_MULTI -dialect SQLITE -sql 'SELECT contour.id, contour.line_length, (ST_intersection(diff.geom, contour.geom)) AS geom FROM diff JOIN contour ON ST_intersects(contour.geom, diff.geom)'")
        os.system(f"ogr2ogr {contoursFile} {contoursFile} -update -dialect SQLITE -sql 'UPDATE contours_cliped SET line_length = ST_Length(geom)'")
        # Remove temp 
        os.system(f"ogr2ogr {contoursFile} {contoursFile} -update -dialect SQL -sql 'DROP TABLE buffer'")
        os.system(f"ogr2ogr {contoursFile} {contoursFile} -update -dialect SQL -sql 'DROP TABLE bbox'")
        os.system(f"ogr2ogr {contoursFile} {contoursFile} -update -dialect SQL -sql 'DROP TABLE diff'")

    # Convert to output format
    os.system(f"ogr2ogr {outputFile} {contoursFile}")

    # Clean up
    os.remove(contoursFile)


def main(argv):
    inputDEM = ''
    outputFile = ''
    interval = ''
    pixelSize = ''
    gaussainBlur = ''
    medianBlur = ''
    contourBuffer = 0

    tmp_file = "resample_dem.tif"
    overwrite = True

    try:
        opts, args = getopt.getopt(argv, "", ["help", "inputDEM=", "outputFile=", "interval=", "pixelSize=", "gaussainBlur=", "medianBlur=", "addContoursBuffer="]) 
    except getopt.GetoptError:
        print("Please look use create_contours.py --help to get more information how to use the script. ")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("--help"):
            print("Create smooth contours with the help of GDAL. Usage:")
            print("\tcreate_contour.py --inputDEM=DEMfile.tif --outputFile=contours.geoJSON --interval=5 --pixelSize=2")
            print("Algorithm for smooth contours in flat areas after: ")
            print("P. Kettunen, C. Koski, and J. Oksanen, 'A design of contour generation for topographic maps with adaptive DEM smoothing' ")
            print("International Journal of Cartography, vol. 3, no. 1, pp. 19–30, Jun. 2017.")
            print("Parameters:")
            print("\t--inputDEM=(rasterFilename)* put here your DEM in any GDAL readable format.")
            print("\t--outputFile=(vectorFilename)* write the name of the outputfile for the contours. The format is guessed form the extention")
            print("\t--interval=(float)* interval between the contour lines.")
            print("\t--pixelSize=(float)* pixel size of the DEM, or a greater number. Used for reampling and should correspond with the aimed map scale")
            print("\t--gaussainBlur={3, 5, 7, 9, 13} kernel size for smoothing flat areas. Default 9.")
            print("\t--medianBlur={3, 5, 7} kernel size for smoothing flat areas. Default is gaussianBlur.")
            print("\t--addContoursBuffer=(float) create addional contour lines in between and cut them to the buffer. Default 0 for no execution.")
            print("\t--help print this hopefully helpfull text.")
            print("\t*necessary for execution.")
            print("Mathias Gröbe 2020")
            sys.exit(0)
        elif opt in ("--inputDEM"):
            inputDEM = arg #dem_file.tif
        elif opt in ("--outputFile"):
            outputFile = arg #contour.sqlite
        elif opt in ("--interval"): 
            interval = arg #5
        elif opt in ("--pixelSize"):
            pixelSize = arg #10
        elif opt in ("--gaussainBlur"):
            gaussainBlur = arg #{3, 5, 7, 9, 13}
        elif opt in ("--medianBlur"):
            medianBlur = arg #{3, 5, 7}            
        elif opt in ("--addContoursBuffer"):
            contourBuffer = arg #50           
    
    if (inputDEM != '') & (outputFile != '') & (interval != '') & (pixelSize != ''):

        # Print info
        print("Create smooth contours with the help of GDAL. ")
        print("----------------------------------------------")
        print("Mathias Gröbe, 2020")
        print("Algorithm for smooth contours in flat areas after: ")
        print("P. Kettunen, C. Koski, and J. Oksanen, 'A design of contour generation for topographic maps with adaptive DEM smoothing' ")
        print("International Journal of Cartography, vol. 3, no. 1, pp. 19–30, Jun. 2017.")
        print("----------------------------------------------")

        # Resample
        os.system("gdal_translate " + inputDEM + " " + tmp_file + " -tr "  + str(pixelSize) + " " + str(pixelSize) + " -r cubic -q")

        # Smooth terrain
        smooth_dem = smoothTerrain(tmp_file, gaussainBlur, medianBlur)

        # Create contour lines file
        print("Create contour lines...")

        if(overwrite):
            try:
                os.remove(outputFile)
                print("Overwrite old file...")
                createContours(outputFile, smooth_dem, interval, contourBuffer)
            except:
                if os.path.isfile(outputFile):
                    print("Can not delete old file! Is it open in a GIS?")
                else:
                    print("Create " + outputFile + ".")
                    createContours(outputFile, smooth_dem, interval)

        # Clean up
        os.remove(tmp_file)
        os.remove(smooth_dem)

    else:
        print("Sorry, missing some information. Please see help.")
        print("create_contour.py --help")
        sys.exit(2)

if __name__ == "__main__":
   main(sys.argv[1:])
