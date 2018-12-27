



import arcpy
folder = 'c://PLANTILLAS_DGAR'
templates = arcpy.GetLayoutTemplatesInfo_server(folder)
print templates
        