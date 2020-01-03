# Name: SplineBarriers.py
# Description: Interpolate a series of point features onto a
#    rectangular raster using a barrier, using a
#    minimum curvature spline technique.
# Requirements: Spatial Analyst Extension and Java Runtime
# Author: Jessica Nephin
# Modified: November 22, 2017 by Cole Fields

# Import system modules
import os
import arcpy
from arcpy import env
from arcpy.sa import *

# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

# barrier shape, cell size, and smoothing option
inBarrierFeature =  r"D:\Projects\NearshoreSubstrate\Data\Boundaries\2.SOG\SalishSea_coast_buffer_1km.shp"
cellSize =  50.0
smoothing = 1

# Set Snap Raster environment
arcpy.env.snapRaster = r'D:\Projects\SpeciesDistributionModeling\_Data\_20m\2.SOG\bathy.tif'

# extent feature
extent = r'D:\Projects\OceanModels\Allen_SalishSeaNEMO_2017\Rasters\20m\circ_sum.tif'

### mask feature
##mask_feature = r'D:\Projects\SpeciesDistributionModeling\_Data\_20m\2.SOG\bathy.tif'

# get extent from extent feature
ext = arcpy.Describe(extent)
ext = ext.extent

# output directory
outdir = r'D:\_TEMP\out2'

# set workspace
env.workspace = r'D:\_TEMP\in'

# get list of shapefiles
shapefiles = arcpy.ListFeatureClasses()

# counter
counter = 1

# loop through each shapefile and interpolate points using spline w/barriers
for shp in shapefiles:
    print('Working on file {} of {}'.format(counter, len(shapefiles)))
    # assign arguments
    fields = arcpy.ListFields(shp)
    zField = fields[2].name
    infeature = shp

    # Execute Spline with Barriers
    print('Executing Spline with Barriers...')
    outSB = SplineWithBarriers(infeature, zField, inBarrierFeature, cellSize, smoothing)

    outname = os.path.splitext(shp)[0] + '.tif'
    outpath = os.path.join(outdir, outname)

    print('Writing {} to {}...'.format(shp, outdir))
    outSB.save(outpath)

    # increment counter
    counter += 1


####################################################################################
## RESAMPLE RASTERS TO 20m / EXTRACT BY MASK
####################################################################################

# Set Snap Raster environment
arcpy.env.snapRaster = r'D:\Projects\SpeciesDistributionModeling\_Data\_20m\2.SOG\bathy.tif'

# set workspace to old out directory
env.workspace = outdir

# list rasters in workspace
rasters = arcpy.ListRasters()

# set new out directory
outdir = r'D:\Projects\OceanModels\Allen_SalishSeaNEMO_2017\Rasters\20m'
##
### masked out directory
##masked_dir = r'D:\Projects\SpeciesDistributionModeling\_Data\_50m'
##
# reset counter
counter = 1

for i in rasters:
    print('Working on file {} of {}'.format(counter, len(rasters)))

    # output file
    outpath = os.path.join(outdir, i)
    print('Resampling {} to 20m and exporting to {}...'.format(i, outdir))
    # Process: Resample
    resample = arcpy.Resample_management(i, outpath, "20 20", "BILINEAR")

##    # extract by mask
##    print('Executing Extract by Mask...')
##    masked_path = os.path.join(masked_dir, i)
##    masked = ExtractByMask(i, mask_feature)
##    masked.save(masked_path)
    # increment counter
    counter += 1









