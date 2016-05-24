###################################################################################
# raster2vector_resume.py script
# 
# Author : Sebastien Peillet
# Project : TAIMPO, UMR Espace Dev
#
# Description : 
# This script is a part of the fire detection processing with MSG data. It could be used with the firemsg.sh 
# script or independantly by launching fire_detect.sh, but don't forget to define the MSG_DATA_PATH environment variable before launching
# script. Example : 'export MSG_DATA_PATH=2016/05/15/1145'
# The script will polygonize raster fire data into point vector. Script built for "resume" raster.
#
# code inspired by the following page : https://pcjericks.github.io/py-gdalogr-cookbook/vector_layers.html
###################################################################################

import os

from osgeo import gdal
from osgeo import ogr
from osgeo import osr
from osgeo import gdal_array
from osgeo import gdalconst

time_path=os.environ["MSG_DATA_PATH"]
time_tab=time_path.split('/')
YYYY=int(time_tab[0])
MM=int(time_tab[1])
DD=int(time_tab[2])
hh=int((time_tab[3])[0:2])
mm=int((time_tab[3])[2:4])


################ POLYGONIZE ####################
# Sub section for polygonize TF

# In data info
inDataFilePath='/home/user/firemsg/Auto/img_TF/'+time_tab[0]+'/'+time_tab[1]+'/'+time_tab[2]+'/'
inDataFileName='LRIT-MSG3-TF-%s%s%s-resume' % (time_tab[0], time_tab[1], time_tab[2])
inDataFile=inDataFilePath+inDataFileName+'.tiff'

# Open TF file
imgTF=gdal.Open(inDataFile)
layerTF=imgTF.GetRasterBand(1)

# Temp data info
tempDriver=ogr.GetDriverByName("ESRI Shapefile")
tempDataFilePath='/home/user/firemsg/Auto/vec_TF/'+time_tab[0]+'/'+time_tab[1]+'/'+time_tab[2]+'/'
try :
    os.makedirs(tempDataFilePath)
except:
	print 'out path already exists'
tempDataFileName='LRIT-MSG3-tvecTF-%s%s%s-resume' % (time_tab[0], time_tab[1], time_tab[2])
tempDataFile=tempDataFilePath+tempDataFileName+'.shp'

if os.path.exists(tempDataFile):
	tempDriver.DeleteDataSource(tempDataFile)

# Create temp data (Source, layer, field)
tempDataSource=tempDriver.CreateDataSource(tempDataFile)
tempDataLayer=tempDataSource.CreateLayer(tempDataFileName, srs=None)
countField=ogr.FieldDefn( "Count", ogr.OFTInteger )
dateField=ogr.FieldDefn( "Date", ogr.OFTDateTime)
tempDataLayer.CreateField(countField)
tempDataLayer.CreateField(dateField)
dst_field = 0

gdal.Polygonize(layerTF,None,tempDataLayer,dst_field,['Count'],callback=None)

for i in range(0, tempDataLayer.GetFeatureCount()):
	# Get the input Feature
	inFeature = tempDataLayer.GetFeature(i)
	inFeature.SetField('Date',int(time_tab[0]),int(time_tab[1]),int(time_tab[2]),0,0,0,0)
	tempDataLayer.SetFeature(inFeature)

################ CLEAN LAYER FROM NON FIRE FEATURE ###########################
# Sub section for clean vector TF, erase non fire polygon, convert polygons into centroids

# Open temp vector TF
#inDriver=ogr.GetDriverByName("ESRI Shapefile")
#inDataSource=inDriver.Open(tempDataFile,1)
#inLayer=inDataSource.GetLayer()

# Apply filter
tempDataLayer.SetAttributeFilter("Count!=0")


# Output data info
outDataFilePath=tempDataFilePath
outDataFileName='LRIT-MSG3-vecTF-%s%s%s-resume' % (time_tab[0], time_tab[1], time_tab[2])
outDatafile=outDataFilePath+outDataFileName+'.shp'
outDriver=ogr.GetDriverByName("ESRI Shapefile")

if os.path.exists(outDatafile):
	outDriver.DeleteDataSource(outDatafile)

outDataSource = outDriver.CreateDataSource(outDatafile)
outLayer = outDataSource.CreateLayer(outDataFileName, geom_type=ogr.wkbPoint)

# Add input Layer Fields to the output Layer
tempDataLayerDefn = tempDataLayer.GetLayerDefn()
for i in range(0, tempDataLayerDefn.GetFieldCount()):
	fieldDefn = tempDataLayerDefn.GetFieldDefn(i)
	outLayer.CreateField(fieldDefn)


# Get the output Layer's Feature Definition
outLayerDefn = outLayer.GetLayerDefn()

# Add features to the ouput Layer
for i in range(0, tempDataLayer.GetFeatureCount()):
    # Get the input Feature
    inFeature = tempDataLayer.GetFeature(i)
    # Create output Feature
    outFeature = ogr.Feature(outLayerDefn)
    # Add field values from input Layer
    for i in range(0, outLayerDefn.GetFieldCount()):
        outFeature.SetField(outLayerDefn.GetFieldDefn(i).GetNameRef(), inFeature.GetField(i))
    # Set geometry as centroid
    geom = inFeature.GetGeometryRef()
    centroid = geom.Centroid()
    outFeature.SetGeometry(centroid)
    # Add new feature to output Layer
    outLayer.CreateFeature(outFeature)

if os.path.exists(tempDataFile):
	outDriver.DeleteDataSource(tempDataFile)