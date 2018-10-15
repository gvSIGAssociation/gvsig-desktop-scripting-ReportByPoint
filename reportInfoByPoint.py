# encoding: utf-8

import gvsig
from gvsig import geom
"""
    print self.__layer.getProperty("reportbypoint.tablenametouse")
    print self.__layer.getProperty("reportbypoint.fields")
    print self.__layer.getProperty("reportbypoint.onerecordreport")
    print self.__layer.getProperty("reportbypoint.typereport")
"""
from org.gvsig.fmap.mapcontext.layers.vectorial import SpatialEvaluatorsFactory
from java.awt.geom import Point2D

def getReportByPoint(self, p):
    layers = gvsig.currentView().getLayers()
    viewProjection = gvsig.currentView().getProjection()
    
    text = """    <!DOCTYPE html>
<html>
<body>
"""
    text+="<p> Report for point: " + str(p) + " </p>"
    for layer in layers:
      if layer.isVisible()== False:
          continue  

      ## Properties
      tableNameToUse = layer.getProperty("reportbypoint.tablenametouse")
      fieldsToUse = layer.getProperty("reportbypoint.fields")
      oneRecord =layer.getProperty("reportbypoint.onerecordreport")
      reportType = layer.getProperty("reportbypoint.typereport")

      
      # DEFAULT VALUES
      if tableNameToUse==None:
        tableNameToUse= layer.getName()
      if fieldsToUse==None:
        if layer.getShapeType()!=geom.SURFACE:
          fieldsToUse= [[attr.getName(), attr.getName(), True] for attr in layer.getFeatureStore().getDefaultFeatureType()]
      if oneRecord==None:
          oneRecord=False
      if reportType==None:
          reportType=0
      ##
      
      text+="<p>"+tableNameToUse+"</p>"

      ## RASTER
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
            value = "Out envelope"
          text+="<th>%s</th>"%(i)
          text+="<th>%s</th>"%(value)
          text+="</tr>"
        text +="""</table>"""
        continue

      ## VECTORIAL
      store = layer.getFeatureStore()
      query = store.createFeatureQuery()
      query.setFilter(SpatialEvaluatorsFactory.getInstance().intersects(p,viewProjection,store))
      #query.setLimit(1)
      for f in fieldsToUse:
          if f[2]==True:
              query.addAttributeName(f[0])
      features = store.getFeatures(query) #,100)
      if len(features) == 0:
        #text += "-- no features found\n"
        text+="""<i>sin entidades</i>"""
        continue
      if oneRecord and len(features) > 1:
        #text += "-- more than one feature\n"
        text+="""<i>más de una entidad seleccionada</i>"""
        continue
      #if reportType
      text +="""<table style="width:100%">"""
      for f in features:
        #text += "--"
        #import pdb
        #pdb.set_trace()
        
        text+= "<tr>"
        for field in fieldsToUse:
          text+="<th>%s</th>"%(field[1])
        text+="</tr>"
        text+="<tr>"
        for field in fieldsToUse:
          nameField = field[0]
          showField = field[1]
          if nameField == "GEOMETRY":
            value = f.get(nameField) #.convertToWKT()
          else:
            value = f.get(nameField)
          #text += showField + ": " + str(value) + ", "
          
          text+="<th>%s</th>"%(value)
        #text += "\n"
        text+="</tr>"
      text+="</table>"
    text+="""</body>
</html>"""
    return text

import gvsig
from gvsig.libs.formpanel import FormPanel

class Panel(FormPanel):
    def __init__(self):
        FormPanel.__init__(self, gvsig.getResource(__file__, "reportbypointpanelreport.xml"))
        self.txpReport.setContentType("text/html")
    def setReportHTML(self, html):
        self.txpReport.setText(html)
        
def main(*args):
    #p = geom.createPoint2D(608992.044, 4721141.865)
    p = geom.createPoint2D(779462, 4723160)
    p = geom.createPoint2D(0.4445681294, 42.562040941311)
    l = Panel()
    l.showTool("Visual")
    content = getReportByPoint(None, p)
    print content
    l.setReportHTML(content)

def main1(*args):
    p = geom.createPoint2D(779462, 4723160)
    
    view = gvsig.currentView()
    layers = view.getLayers()
    for l in layers:
        if l.getShapeType()==geom.SURFACE:
            at = l.getDataStore().getAffineTransform()
            from java.awt.geom import Point2D
            preal = Point2D.Double(p.getX(), p.getY())
            px = Point2D.Double()
    
            at.inverseTransform(preal, px)
            x=int(px.getX())
            y=int(px.getY())
            print x,y
            for i in range(0,l.getDataStore().getBandCount()):
              print "i:",i, " value:", l.getDataStore().getData(x,y,i)
            print px
