# encoding: utf-8

import gvsig
from gvsig import geom
from java.awt.geom import Point2D
from org.gvsig.fmap.mapcontrol.tools.Listeners import PointListener
#from org.gvsig.fmap.mapcontrol.tools.Behavior import MouseMovementBehavior
#from org.gvsig.fmap.mapcontrol.tools.Listeners import AbstractPointListener
from org.gvsig.fmap.mapcontext.layers.vectorial import SpatialEvaluatorsFactory
from org.gvsig.fmap import IconThemeHelper
import reportbypointpanelreport
reload(reportbypointpanelreport)
from addons.ReportByPoint.reportbypointpanelreport import ReportByPointPanelReport
from org.gvsig.fmap.mapcontrol.tools.Behavior import PointBehavior
from org.gvsig.tools import ToolsLocator
from addons.ReportByPoint.rbplib.getHTMLReportByPoint import getHTMLReportByPoint

class ReportByPoint(object):

  def __init__(self):
    self.__behavior = None
    self.__layer = None

  def getTooltipValue(self, point, projection):
    return ""

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
    content = getHTMLReportByPoint(p, self.mapControl)
    return content
    
  def showReport(self, event):
    p = event.getMapPoint()
    #tip = self.reportbypoint.getTooltipValue(p,self.projection)
    #self.mapControl.setToolTipText(unicode(tip, 'utf-8'))
    #from addons.ScriptingComposerTools.javadocviewer.webbrowserpanel import BrowserPanel
    #p = BrowserPanel()
    report = ReportByPointPanelReport()
    i18nManager =ToolsLocator.getI18nManager()
    report.showTool(i18nManager.getTranslation("_Report_by_point_info"))
    content = self.getReportByPoint(p)
    report.setHTMLText(content)
    #print content

    
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
  
  reportbypoint = ReportByPoint()
  reportbypoint.setTool(mapControl)
  
