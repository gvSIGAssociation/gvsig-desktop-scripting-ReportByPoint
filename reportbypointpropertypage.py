# encoding: utf-8

import gvsig

from org.gvsig.propertypage import PropertiesPage
from org.gvsig.fmap.mapcontext.layers.vectorial import VectorLayer
from org.gvsig.app.project.documents.view import ViewDocument
from org.gvsig.propertypage import PropertiesPageFactory
from org.gvsig.fmap.mapcontrol import MapControlLocator

import reportbypointpanel
reload(reportbypointpanel)
from reportbypointpanel import ReportByPointPanel

from org.gvsig.tools import ToolsLocator

class ReportByPointPropertyPage(PropertiesPage):

  def __init__(self, layer=None):
    self.__panel = ReportByPointPanel(layer)
      
  def getTitle(self):
    i18n = ToolsLocator.getI18nManager()
    return i18n.getTranslation("_Reportbypoint")

  def asJComponent(self):
    return self.__panel.asJComponent()
  
  def getPriority(self):
    return 1

  def whenAccept(self):
    self.__panel.save()
    return True

  def whenApply(self):
    return self.whenAccept()

  def whenCancel(self):
    return True

class ReportByPointPropertyPageFactory(PropertiesPageFactory):

  def __init__(self):
    pass

  def getName(self):
    return "Reportbypoint"
    
  def getGroupID(self):
    return ViewDocument.LAYER_PROPERTIES_PAGE_GROUP
    
  def isVisible(self, layer):
    if isinstance(layer,VectorLayer):
      return True
    return False

  def create(self, object1, layer):
    if not isinstance(layer,VectorLayer):
      return None
    return ReportByPointPropertyPage(layer)

def selfRegister():
  propertiesPageManager = MapControlLocator.getPropertiesPageManager()
  propertiesPageManager.registerFactory(ReportByPointPropertyPageFactory())

def main(*args):
  selfRegister()
    