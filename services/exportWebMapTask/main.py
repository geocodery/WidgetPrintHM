import sys
# ONLY USE IN GEOPROCESSIN SERVICE
sys.path.insert(0, r'D:\\aplicativos\\geoprocesos\\exportWebMapTask')

import json
import arcpy
import os
import uuid
import time

arcpy.env.overwriteOutput = True

# directorio = r'D:\RYali\TDR3\3Product')
directorio = r'C:\plantillas_dgar'

class exportWebMapTask(object):
    def __init__(self, Web_Map_as_JSON, Format, Layout_Template):
        self.wmj         = Web_Map_as_JSON
        self.format      = Format
        self.lyttemplate = Layout_Template

        arcpy.AddMessage(self.wmj)
        arcpy.AddMessage(self.format)
        arcpy.AddMessage(self.lyttemplate)

    def acondicionaJson(self, dicc):
        arcpy.AddMessage(dicc)
        for x in dicc["operationalLayers"]:
            if x.has_key("featureCollection"):
                if x["featureCollection"].has_key("layers"):
                    for m in x["featureCollection"]["layers"]:
                        if m.has_key("featureSet"):
                            if m["featureSet"].has_key("features"):
                                for n in m["featureSet"]["features"]:
                                    if n.has_key("symbol"):
                                        symbol = "symbol" if n["symbol"].has_key("color") else ""
                                        outline_tmp = n["symbol"]["outline"] if n["symbol"].has_key("outline") else {
                                            "msg": "msg"}
                                        outline = "outline" if outline_tmp.has_key("color") else ""
                                        info = [symbol, outline]
                                        for x in info:
                                            if x == "symbol":
                                                n["symbol"]["color"] = ["220", "220", "220", "255"]
                                            elif x == "outline":
                                                n["symbol"]["outline"]["color"] = ["220", "220", "220", "255"]
        outputJson = json.dumps(dicc)
        arcpy.AddMessage(outputJson)
        return outputJson

    def extractTitleMap(self):
        if self.wmj not in ("", "#"):
            dicc = json.loads(self.wmj)
            self.wmj = self.acondicionaJson(dicc)
        else:
            dicc = {"msg": "true"}
        self.maptitle = dicc["layoutOptions"]['titleText'] if dicc.has_key("layoutOptions") else "ArcGIS Web Map"
        arcpy.AddMessage(self.maptitle)

    def seleccionarPlantilla(self):
        if self.lyttemplate == '#' or not self.lyttemplate:
            self.lyttemplate = 'A4-Horizontal'

        if self.format == "#" or not self.format:
            self.format = "PDF"

        template_mxd = os.path.join(directorio, '{}.mxd'.format(self.lyttemplate))
        proyecto = arcpy.mapping.ConvertWebMapToMapDocument(self.wmj, template_mxd)
        self.mxd = proyecto.mapDocument
        self.df = arcpy.mapping.ListDataFrames(self.mxd)[0]

    def almacenarCopiaMXD(self, name):
        copia = os.path.join("D:\\aplicativos\\geoprocesos\\exportWebMapTask", 'Map{}.mxd'.format(name))
        self.mxd.saveACopy(copia)

    def exportarMapa(self):
        namepdf = str(uuid.uuid4())
        if self.format == "PDF":
            salida = os.path.join(arcpy.env.scratchFolder, 'Map{}.pdf'.format(namepdf))
            arcpy.mapping.ExportToPDF(self.mxd, salida, "PAGE_LAYOUT")
        else:
            salida = os.path.join(arcpy.env.scratchFolder, 'Map{}.png'.format(namepdf))
            arcpy.mapping.ExportToPNG(self.mxd, salida, "PAGE_LAYOUT", resolution=200)
        self.almacenarCopiaMXD(namepdf)
        return salida


    # ***************************************************************************
    def aobjIntervals(self):
        import comtypes
        import comtypes.server.localserver
        from comtypes.client import GetModule, CreateObject
        import arcpy.mapping as mp
        from snippets102 import GetStandaloneModules, InitStandalone
        esriCarto = GetModule(r"D:\geoprocesos\config\esriCarto.olb")
        GetStandaloneModules()
        InitStandalone()

        self.mxdObject = CreateObject(esriCarto.MapDocument, interface=esriCarto.IMapDocument)
        self.mxdObject.Open(mxd_path)
        IMap = self.mxdObject.ActiveView.FocusMap
        activeView = self.mxdObject.ActiveView
        pageLayout = activeView.QueryInterface(esriCarto.IPageLayout)
        graphicsContainer = pageLayout.QueryInterface(esriCarto.IGraphicsContainer)
        frameElement = graphicsContainer.FindFrame(IMap)
        mapFrame = frameElement.QueryInterface(esriCarto.IMapFrame)
        mapGrids = mapFrame.QueryInterface(esriCarto.IMapGrids)
        [mapGrids.MapGrid(i) for i in xrange(mapGrids.MapGridCount)]

        grids = [mapGrids.MapGrid(i) for i in xrange(mapGrids.MapGridCount)]

        for g in grids:
            print g.Name, g.Visible
            g.Visible = False

        self.mxdObject.Save()

    def defineIntervals(self):
        arcpy.AddMessage("Definir intervalos")


    # ***************************************************************************

    def main(self):
        # self.aobjIntervals()
        self.extractTitleMap()
        self.seleccionarPlantilla()
        Output_File = self.exportarMapa()
        arcpy.SetParameterAsText(3, Output_File)
