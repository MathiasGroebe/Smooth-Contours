#!/usr/bin/env python

import os
import re
import string
import random


demFile = "334245636_dgm1.tif"
intervall = 10
pixelSize = 10
name = "contour"
tmp_file = "resample_dem.tif"


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
    if (smooth == 13):
        os.system('gdal_calc.py -A ' + prefix + '_tpi_norm.tif -B ' + prefix + '_dem_blur_3x3.vrt -C ' + prefix + '_dem_blur_13x13.vrt --outfile="smooth_' + inputDEM + '" --overwrite --calc="A*B+(1-A)*C"')
    else:
        os.system('gdal_calc.py -A ' + prefix + '_tpi_norm.tif -B ' + prefix + '_dem_blur_3x3.vrt -C ' + prefix + '_dem_blur_13x13.vrt --outfile="smooth_' + inputDEM + '" --overwrite --calc="A*B+(1-A)*C"')

    # Clean up
    os.remove(prefix + "_dem.tif")
    os.remove(prefix + "_dem_tpi.tif")
    os.remove(prefix + "_dem_blur_3x3.vrt")
    os.remove(prefix + "_dem_blur_9x9.vrt")
    os.remove(prefix + "_dem_blur_13x13.vrt")
    os.remove(prefix + "_tpi_pos.tif")
    os.remove(prefix + "_tpi_pos.tif.aux.xml")
    os.remove(prefix + "_tpi_blur_3x3.vrt")
    os.remove(prefix + "_tpi_norm.tif")

    return("smooth_" + inputDEM)

def main():
    # Resample
    os.system("gdal_translate " + demFile + " " + tmp_file + " -tr "  + str(pixelSize) + " " + str(pixelSize) + " -r cubic")

    # Smooth terrain
    smooth_dem = smoothTerrain(tmp_file, 13)

    print("Create contour lines...")
    os.system("gdal_contour -inodata -snodata -32768 -a ele "  + smooth_dem + " " + name + ".sqlite -nln smooth_contour -i " + str(intervall))

    # Clean up
    os.remove(tmp_file)
    os.remove(smooth_dem)

if __name__ == "__main__":
    main()
