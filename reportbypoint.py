# encoding: utf-8

import gvsig
from gvsig import geom
from java.awt.geom import Point2D
from org.gvsig.fmap.mapcontrol.tools.Listeners import PointListener
#from org.gvsig.fmap.mapcontrol.tools.Behavior import MouseMovementBehavior
#from org.gvsig.fmap.mapcontrol.tools.Listeners import AbstractPointListener
from org.gvsig.fmap.mapcontext.layers.vectorial import SpatialEvaluatorsFactory
from org.gvsig.fmap import IconThemeHelper
from addons.ReportByPoint.reportbypointpanelreport import ReportByPointPanelReport
from org.gvsig.fmap.mapcontrol.tools.Behavior import PointBehavior

class ReportByPoint(object):

  def __init__(self):
    self.__behavior = None
    self.__layer = None

  def getTooltipValue(self, point, projection):
    return "tooltip"

  def setTool(self, mapControl):
    actives = mapControl.getMapContext().getLayers().getActives()
    if len(actives)!=1:
      # Solo activamos la herramienta si hay una sola capa activa
      #print "### reportbypoint.setTool: active layers != 1 (%s)" % len(actives)
      return
    #mode = actives[0].getProperty("reportbypoint.mode")
    #if mode in ("", None):
    #  # Si la capa activa no tiene configurado el campo a mostrar
    #  # tampoco activamos la herramienta
    #  #print '### reportbypoint.setTool: active layer %s not has property "reportbypoint.fieldname"' % actives[0].getName()
    #  return 
    self.__layer = actives[0]
        
    #if it has the tool
    if not mapControl.hasTool("reportbypoint"):
      #print '### QuickInfo.setTool: Add to MapControl 0x%x the "quickinfo" tool' % mapControl.hashCode()
      #
      # Creamos nuestro "tool" asociando el MouseMovementBehavior con nuestro
      # QuickInfoListener.
      #self.__behavior = MouseMovementBehavior(ReportByPointListener(mapControl, self))
      self.__behavior = PointBehavior(ReportByPointListener(mapControl, self))
      #self.__behavior.setMapControl(mapControl)    
      #
      # Le añadimos al MapControl la nueva "tool".
      mapControl.addBehavior("reportbypoint", self.__behavior)
    #print '### QuickInfo.setTool: setTool("quickinfo") to MapControl 0x%x' % mapControl.hashCode()
    #
    # Activamos la tool.
    
    mapControl.setTool("reportbypoint")
    

class ReportByPointListener(PointListener):

  def __init__(self, mapControl, reportbypoint):
    PointListener.__init__(self)
    self.mapControl = mapControl
    self.reportbypoint = reportbypoint
    self.projection = self.mapControl.getProjection()

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
    
  def showReport(self, event):
    p = event.getMapPoint()
    #tip = self.reportbypoint.getTooltipValue(p,self.projection)
    #self.mapControl.setToolTipText(unicode(tip, 'utf-8'))
    #from addons.ScriptingComposerTools.javadocviewer.webbrowserpanel import BrowserPanel
    #p = BrowserPanel()
    report = ReportByPointPanelReport()
    content = self.getReportByPoint(p)
    report.setHTMLText(content)
    report.showTool("ReportByPointPanelReport")
    #p.setContent(content)
    #p.showWindow()

    
  def point(self, event):
    self.showReport(event)
    
  def pointDoubleClick(self, event):
    self.showReport(event)
  def getImageCursor(self):
    """Evento de PointListener"""
    return IconThemeHelper.getImage("cursor-select-by-point")

  def cancelDrawing(self):
    """Evento de PointListener"""
    return False

def main(*args):      
  viewDoc = gvsig.currentView()
  viewPanel = viewDoc.getWindowOfView()
  mapControl = viewPanel.getMapControl()
  
  quickInfo = ReportByPoint()
  quickInfo.setTool(mapControl)
