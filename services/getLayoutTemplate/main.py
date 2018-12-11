import sys
# ONLY USE IN GEOPROCESSIN SERVICE
sys.path.insert(0, r'D:\\aplicativos\\geoprocesos\\getLayoutTemplate')

import arcpy
import json
import os

arcpy.env.overwriteOutput = True

class GetTemplates(object):
    def __init__(self, folderTemplate):
        self.folder = folderTemplate

    def GetTemplatesInfo(self):
        templates = arcpy.GetLayoutTemplatesInfo_server(self.folder)
        j = json.dumps(templates[0])
        j2 = j.replace("activeDataFrameSize", "webMapFrameSize")
        j3 = json.loads(j2)
        return j3

    def process(self):
        templates = self.GetTemplatesInfo()
        arcpy.SetParameterAsText(1, templates)

    def main(self):
        if self.folder in ("#", "0", 0, None, ""):
            pass
        else:
            self.process()

# if __name__ == "__main__":
#     poo = ConsultaTematica()
#     poo.main() 