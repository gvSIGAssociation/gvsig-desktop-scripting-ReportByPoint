# encoding: utf-8

import gvsig

import os.path

from os.path import join, dirname

from gvsig import currentView
from gvsig import currentLayer

from java.io import File

from org.gvsig.app import ApplicationLocator
from org.gvsig.andami import PluginsLocator
from org.gvsig.scripting.app.extension import ScriptingExtension
from org.gvsig.tools.swing.api import ToolsSwingLocator

from reportbypoint import ReportByPoint
  
from org.gvsig.tools import ToolsLocator
## icons author
## <div>Icons made by 
## <a href="https://www.freepik.com/" title="Freepik">Freepik</a> 
## from <a href="https://www.flaticon.com/"          
## title="Flaticon">www.flaticon.com</a> is licensed by 
## <a href="http://creativecommons.org/licenses/by/3.0/"   
## title="Creative Commons BY 3.0" target="_blank">CC 3.0 BY</a></div>
class ReportByPointExtension(ScriptingExtension):
  def __init__(self):
    pass

  def isVisible(self):
    return True

  def isLayerValid(self, layer):
    #if layer == None:
    #  #print "### reportbypointExtension.isLayerValid: None, return False"
    #  return False
    #mode = layer.getProperty("reportbypoint.mode")
    #if mode in ("", None):
    #  # Si la capa no tiene configurado el campo a mostrar
    #  # no activamos la herramienta
    #  return False
    return True
    
  def isEnabled(self):
    layer = currentLayer()
    #if not self.isLayerValid(layer):
    #  return False
    return True

  def execute(self,actionCommand, *args):
    actionCommand = actionCommand.lower()
    if actionCommand == "settool-reportbypoint":
      #print "### QuickinfoExtension.execute(%s)" % repr(actionCommand)
      layer = currentLayer()
      if not self.isLayerValid(layer):
        return
      viewPanel = currentView().getWindowOfView()
      mapControl = viewPanel.getMapControl()
      reportbypoint = ReportByPoint()
      reportbypoint.setTool(mapControl)

def selfRegister():
  i18n = ToolsLocator.getI18nManager()
  application = ApplicationLocator.getManager()
  actionManager = PluginsLocator.getActionInfoManager()
  iconTheme = ToolsSwingLocator.getIconThemeManager().getCurrent()

  quickinfo_icon = File(gvsig.getResource(__file__,"images","reportbypoint1.png")).toURI().toURL()
  iconTheme.registerDefault("scripting.reportbypoint", "action", "tools-reportbypoint", None, quickinfo_icon)

  reportbypoint_extension = ReportByPointExtension()
  reportbypoint_action = actionManager.createAction(
    reportbypoint_extension,
    "tools-reportbypoint",   # Action name
    "Show report by point",   # Text
    "settool-reportbypoint", # Action command
    "tools-reportbypoint",   # Icon name
    None,                # Accelerator
    1009000000,          # Position
    i18n.getTranslation("_Report_by_point_info")    # Tooltip
  )
  reportbypoint_action = actionManager.registerAction(reportbypoint_action)

  # Añadimos la entrada "Quickinfo" en el menu herramientas
  application.addMenu(reportbypoint_action, "tools/_ReportByPoint")
  # Añadimos el la accion como un boton en la barra de herramientas "Quickinfo".
  application.addSelectableTool(reportbypoint_action, "ReportByPoint")

def main(*args):
  selfRegister()
  