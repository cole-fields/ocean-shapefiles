#########################################################################################################################################################
#-------------------------------------------------------------------------------------------------------------------------------------------------------#
'''
 NAME:          resample
 PURPOSE:       arcpy resample funciton

 DATE:          March 14, 2019

 AUTHOR:        Cole Fields
                Spatial Analyst
                Marine Spatial Ecosystem Analysis (MSEA)
                Fisheries and Oceans Canada
'''
#-------------------------------------------------------------------------------------------------------------------------------------------------------#


# Import system modules
import os
import arcpy
from arcpy import env
from arcpy.sa import *

# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

mask = r'D:\Projects\ModellingDomains\Data\bounding_boxes.gdb\hg_20m_2kmbuffer'
wd = r'D:\Projects\OceanModels\BC_ROMS\Data\Bottom_Rasters'
snap = r'D:\Projects\OceanModels\BC_ROMS\Data\Bottom_Rasters\BottomCirculationCurrentSpeed_max.tif'
resample_snap = r'D:\Projects\NearshoreSubstrate\Data\Predictors\4.HG\bathy.tif'
out = r'D:\_processing\Masked\hg'
resample_out = 'D:\_processing\Resampled\hg'
resample_wd = out
res = 20

## extract by mask
def extract_mask(mask, wd, snap, out):
    try:
        # set workspace
        env.workspace = wd

        # list rasters in workspace
        rasters = arcpy.ListRasters()

        # Set Snap Raster environment
        arcpy.env.snapRaster = snap

        # counter
        counter = 1

        # list of layers
        layers = []

        for i in rasters:
            print('Working on file {} of {}'.format(counter, len(rasters)))

            # extract by mask
            print('Executing Extract by Mask...')
            masked_path = os.path.join(out, i)
            masked = ExtractByMask(i, mask)
            masked.save(masked_path)

            # append layer to list
            layers.append(masked)

            # increment counter
            counter += 1

    ## PRINT ERRORS IF THE FUNCTION FAILED
    except arcpy.ExecuteError:
        msgs        = arcpy.GetMessages(2)                                                                  # get the tool error messages
        print(msgs)                                                                                         # return tool error messages for use with a script tool
    except:
        tb          = sys.exc_info()[2]                                                                     # get traceback object
        tb_info     = traceback.format_tb(tb)[0]                                                            # concatenate info together re error into message string
        pymsg       = 'PYTHON ERRORS: \nTraceback info: \n' + tb_info + '\nError Info: \n' + str(sys.exc_info()[1])
        msgs        = 'ArcPy ERRORS: \n' + arcpy.GetMessages(2) + '\n'
        print(pymsg)                                                                                        # return python error messages for use in script tool
        print(msgs)
    return layers

## resample raster to new resolution
def resample_raster(wd, res, snap, out):
    try:
        # set workspace
        env.workspace = wd

        # list rasters in workspace
        rasters = arcpy.ListRasters()

        # Set Snap Raster environment
        arcpy.env.snapRaster = snap

        # counter
        counter = 1

        for i in rasters:
            print('Working on file {} of {}'.format(counter, len(rasters)))

            # output file
            outpath = os.path.join(out, i)
            print('Resampling {} to {} and exporting to {}...'.format(i, res, out))

            # Process: Resample
            arcpy.Resample_management(i, outpath, str(res), "BILINEAR")

            # increment counter
            counter += 1

    ## PRINT ERRORS IF THE FUNCTION FAILED
    except arcpy.ExecuteError:
        msgs        = arcpy.GetMessages(2)                                                                  # get the tool error messages
        print(msgs)                                                                                         # return tool error messages for use with a script tool
    except:
        tb          = sys.exc_info()[2]                                                                     # get traceback object
        tb_info     = traceback.format_tb(tb)[0]                                                            # concatenate info together re error into message string
        pymsg       = 'PYTHON ERRORS: \nTraceback info: \n' + tb_info + '\nError Info: \n' + str(sys.exc_info()[1])
        msgs        = 'ArcPy ERRORS: \n' + arcpy.GetMessages(2) + '\n'
        print(pymsg)                                                                                        # return python error messages for use in script tool
        print(msgs)
    return



masked = extract_mask(mask, wd, snap, out)
res = resample_raster(resample_wd, res, resample_snap, resample_out)




