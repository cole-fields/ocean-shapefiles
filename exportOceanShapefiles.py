import arcpy
import os

outdir = r'E:\Projects\OceanModels\BC_ROMS\Data\Bottom_Shapefiles'

# set workspace
arcpy.env.workspace = outdir

# list datasets
l = arcpy.ListFeatureClasses()

# empty list
fieldnames = []

# populate list with field names
for i in arcpy.ListFields(l[0]):
    fieldnames.append(i.name)

# drop extra fields
fieldnames = fieldnames[3:]

# make copy of feature classes with value name appended (i.e. circulation_min)
for i in l:
    for j in fieldnames:
        name = i[:-4] + '_' + j
        arcpy.FeatureClassToFeatureClass_conversion(in_features=i, out_path=outdir, out_name=name)


# now delete fields except for value field
arcpy.env.workspace = r'C:\TEMP'
os.chdir(r'C:\TEMP')
# list feature classes
fcs = arcpy.ListFeatureClasses(r'C:\Users\fieldsc\PycharmProjects\untitled')

fcs = arcpy.ListFeatureClasses()

# for each item, get the value name (min, max, etc)
for fc in fcs:
    # get name of value for layer (min, max, etc)
    value = str(fc).split('_')[1][:-4]
    # empty list for field names
    fields = []
    for field in arcpy.ListFields(fc):
        fields.append(field.name)
    print('There are {} fields in {}...\n'
          'Field names are: {}'.format(len(fields), fc, fields))
    keeps = ["FID", "Shape", value]
    print('Keeping the following fields: {}'.format(keeps))
    # keep not-deletable fields and the value fields in list
    drops = [x for x in fields if x not in keeps]
    print('Deleting the following fields: {}'.format(drops))
    if len(drops) > 0:
        # delete fields in drops list from fc
        arcpy.DeleteField_management(fc, drops)
