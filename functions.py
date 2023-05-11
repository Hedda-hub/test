# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 09:56:52 2023

@author: bonatz
"""
import os
from osgeo import gdal


def reclass(*args):
    # open raster with gdal
    file = gdal.Open(raster) # DEM 
    print(file)
    # get raster band
    band = file.GetRasterBand(1)
    # read raster band as array
    array = band.ReadAsArray()
    ndval=band.GetNoDataValue()
    driver = gdal.GetDriverByName('GTiff') # define prefered driver

    # 1. RECLASSIFY RASTER ACCORDING TO ELEVATION
    
    print('1. Reclassifying '+str(file))
    
    # reclassification according to elevation increment
    array[array <= value] = value
    array[array > value] = ndval
    
    # create new empty raster and write reclassified array to it
    file2 = driver.Create(outfile, 
                          file.RasterXSize , 
                          file.RasterYSize , 1 , 
                          gdal.GDT_Byte) # GDT_Byte = uint8 (int 0-255)
    file2.GetRasterBand(1).SetNoDataValue(ndval)
    file2.GetRasterBand(1).WriteArray(array)
    
    # spatial ref system
    # define metadata --> here the metadata of the original raster is used for
    # the new raster
    proj = file.GetProjection() # get projection
    georef = file.GetGeoTransform() # get boundaries
    file2.SetProjection(proj) # set projection
    file2.SetGeoTransform(georef) # set boundaries
    file2.GetRasterBand(1).SetNoDataValue(ndval) # set no data values
    file2.FlushCache() # close file
    
    print('Done with reclassification '+str(file2))


os.chdir(r'D:\CoCliCo\MA\Data\test')

elevation_list=[6,7]
for value in elevation_list:
    
    raster= r'D:\CoCliCo\MA\Data\test\MeritDEM_n30e000.tif'
    outfile=r'D:\CoCliCo\MA\Data\test\MeritDEM_reclass_'+str(value)+'.tif'
    reclass(raster,outfile)

