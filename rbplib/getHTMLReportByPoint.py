# encoding: utf-8

import gvsig
from gvsig import geom

from java.awt.geom import Point2D
from org.gvsig.fmap.mapcontext.layers.vectorial import SpatialEvaluatorsFactory
from org.gvsig.tools import ToolsLocator
from addons.ReportByPoint.reportbypointpanelreport import ReportByPointPanelReport

def main(*args):
    p = geom.createPoint2D(0.4445681294, 42.562040941311)
    mapControl = gvsig.currentView().getMainWindow().getMapControl()
    content = getHTMLReportByPoint(p, mapControl)
    r = ReportByPointPanelReport()
    r.showTool("Visual")
    r.setHTMLText(content)
    
def getHTMLReportByPoint(p, mapControl):
    layers = gvsig.currentView().getLayers()
    viewProjection = gvsig.currentView().getProjection()
    
    text = """    <!DOCTYPE html>
<html>
<body>
"""
    i18nManager = ToolsLocator.getI18nManager()
    textReportForPoint = str(i18nManager.getTranslation("_Report_for_point"))
    text+="<p> "+textReportForPoint+" "+ str(p) + " </p>"
    for layer in layers:
      if layer.isVisible()== False:
          continue  

      ## Properties
      tableNameToUse = layer.getProperty("reportbypoint.tablenametouse")
      fieldsToUse = layer.getProperty("reportbypoint.fields")
      oneRecord =layer.getProperty("reportbypoint.onerecordreport")
      reportType = layer.getProperty("reportbypoint.typereport")

      
      ## DEFAULT VALUES
      if tableNameToUse==None:
        tableNameToUse= layer.getName()
      if fieldsToUse==None:
        if layer.getShapeType()!=geom.SURFACE:
          fieldsToUse= [[attr.getName(), attr.getName(), True] for attr in layer.getFeatureStore().getDefaultFeatureType()]
      if oneRecord==None:
          oneRecord=False
      if reportType==None:
          reportType=0
      
      ###
      ### Clean fieldToUse
      ###
      justFieldsToShow = []
      for field in fieldsToUse:
        if field[2]==True:
          justFieldsToShow.append(field)
          

      ## INIT HTML
      text+="<p>"+tableNameToUse+"</p>"
      
      ##
      ## RASTER INFO
      ##
      if layer.getShapeType()==geom.SURFACE:
         ## Fixed projection
        layerProjection=layer.getProjection()
        pointAnalysis = p.cloneGeometry()
        if layerProjection == viewProjection:
          pass
        else:
          ICoordTrans1 = viewProjection.getCT(layerProjection)
          pointAnalysis.reProject(ICoordTrans1)
        text +="""<table style="width:100%">"""
        store = layer.getDataStore()
        at = store.getAffineTransform()
        
        preal = Point2D.Double(pointAnalysis.getX(), pointAnalysis.getY())
        px = Point2D.Double()

        at.inverseTransform(preal, px)
        x=int(px.getX())
        y=int(px.getY())
        text+= "<tr>"
        for field in ["Band", "Value"]:
          text+="<th>%s</th>"%(field)
        text+="</tr>"
        
        for i in range(0,store.getBandCount()):
          text+= "<tr>"
          try:
            value = store.getData(x,y,i)
          except:
            value = str(i18nManager.getTranslation("_Out_of_envelope"))
          text+="<th>%s</th>"%(i)
          text+="<th>%s</th>"%(value)
          text+="</tr>"
        text +="""</table>"""
        continue
      
      ## (rest of values are vectorial)
      ## VECTORIAL INFO
      ##
      layerTolerance = layer.getDefaultTolerance()
      tolerance = mapControl.getViewPort().toMapDistance(layerTolerance)
      pBufferTolerance = p.buffer(tolerance)
                    
      store = layer.getFeatureStore()
      query = store.createFeatureQuery()
      query.setFilter(SpatialEvaluatorsFactory.getInstance().intersects(pBufferTolerance,viewProjection,store))
      #query.setLimit(1)
      for f in justFieldsToShow: # [attr.getName(), attr.getName(), True] 
        query.addAttributeName(f[0])
      features = store.getFeatureSet(query) #,100)

      if features.getSize() == 0:
        textNoFeatures = i18nManager.getTranslation("_No_features")
        text+="""<i>%s</i>"""%(textNoFeatures)
        continue
      if oneRecord and features.getSize() > 1:
        textMoreThanOne=i18nManager.getTranslation("_More_than_one_selected")
        text+="""<i>%s</i>"""%(textMoreThanOne)
        continue
      if reportType==0: ### TABLE FORMAT
        text +="""<table style="width:100%">"""
        firstIteration=0
        for f in features:
          if firstIteration==0:
            text+= "<tr>"
            for field in justFieldsToShow: #[attr.getName(), attr.getName(), True] 
              text+="<th>%s</th>"%(field[1])
            text+="</tr>"
            firstIteration+=1
          text+="<tr>"
          for field in justFieldsToShow:
            nameField = field[0]
            #showField = field[1]
            if nameField == "GEOMETRY":
              value = f.get(nameField) #.convertToWKT()
            else:
              value = f.get(nameField)
            text+="<th>%s</th>"%(value)
          text+="</tr>"
        text+="</table>"
      elif reportType==1: ### TWO COLUMNS
        text +="""<table style="width:100%">"""
        for field in justFieldsToShow: #[attr.getName(), attr.getName(), True] 
          nameField = field[0]
          showField = field[1]
          text+="<tr>"
          text+="<th>%s</th>"%(showField)
          for f in features:
            if nameField == "GEOMETRY":
              value = f.get(nameField) #.convertToWKT()
            else:
              value = f.get(nameField)
            text+="<th>%s</th>"%(value)
          text+="</tr>"
        text+="</table>"
    text+="""</body>
</html>"""
    return text