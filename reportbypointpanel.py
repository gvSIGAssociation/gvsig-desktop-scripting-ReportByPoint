# encoding: utf-8

import gvsig
from gvsig import getResource
from gvsig.libs.formpanel import FormPanel

from org.gvsig.tools.swing.api import ToolsSwingLocator
from javax.swing import DefaultListModel
from java.awt.event import MouseEvent
from javax.swing import ButtonGroup

import sys

from org.gvsig.fmap.dal import DALLocator
from org.gvsig.tools.evaluator import EvaluatorData

from java.lang import Double
from java.net import URI
from org.gvsig.tools import ToolsLocator
from java.util import Date
from java.net import URL
from java.math import BigDecimal
from java.lang import Float
from java.io import File
from org.gvsig.tools.dataTypes import DataTypes
from javax.swing.table import DefaultTableModel
from javax.swing import JTable
from org.gvsig.tools.evaluator import EvaluatorException
from java.lang import Boolean, String
from javax.swing import JScrollPane
from javax.swing import ScrollPaneConstants
from java.awt import BorderLayout
from java.awt.geom import Point2D
from java.lang import Object

class MyDefaultTableModel(DefaultTableModel):
  def isCellEditable(self, row, column):
    if column==0:
      return False
    else:
      return True
      
class ReportFormatType(Object):
  def __init__(self, name, rtype):
    self.name = name
    self.rtype = rtype
    
  def getName(self):
    return self.name
    
  def getFormatType(self):
    return self.rtype

  def toString(self):
    return  str(self.getName())
    
class FieldsPropertiesTable(JTable):
  def __init__(self, model):
    self.setModel(model)
    
  def getColumnClass(self, column):
    if column==2:
        return Boolean
    else:
        return String

class ReportByPointPanel(FormPanel):
  def __init__(self, layer=None):
    FormPanel.__init__(self,getResource(__file__,"reportbypointpanel3.xml"))
    i18Swing = ToolsSwingLocator.getToolsSwingManager()
    i18Swing.translate(self.lblTableNameToUse)
    i18Swing.translate(self.lblFields)
    i18Swing.translate(self.chkOneRecord)
    i18Swing.translate(self.lblTypeOfReport)
    
    self.cboTypeReport.removeAllItems()
    i18nManager = ToolsLocator.getI18nManager()
    
    self.cboTypeReport.addItem(ReportFormatType(i18nManager.getTranslation("_By_table"),0))
    self.cboTypeReport.addItem(ReportFormatType(i18nManager.getTranslation("_With_two_columns"),1))
    
    self.setLayer(layer)
      
  def setLayer(self, layer):
    self.__layer = layer
    ### PROPERTY NAME
    propertyTablenametosue = self.__layer.getProperty("reportbypoint.tablenametouse")
    if propertyTablenametosue==None:
      propertyTablenametosue = self.__layer.getName()
    
    self.txtTableNameToUse.setText(propertyTablenametosue)

    ### PROPERTY FIELDS
    i18nManager = ToolsLocator.getI18nManager()
    columnNames = [
                   i18nManager.getTranslation("_Field_name"),
                   i18nManager.getTranslation("_Name_to_show"),
                   i18nManager.getTranslation("_Show")
                   ]

    propertyFields = self.__layer.getProperty("reportbypoint.fields")
    if propertyFields==None:
      featureType = self.__layer.getFeatureStore().getDefaultFeatureType()
      propertyFields = [[attr.getName(), attr.getName(), True] for attr in featureType]

    model = MyDefaultTableModel(propertyFields, columnNames)

    table = FieldsPropertiesTable(model)
    table.setAutoResizeMode(3)
    #table.getColumnModel().getColumn(0).setPreferredWidth(50)
    #table.getColumnModel().getColumn(1).setPreferredWidth(50)
    #table.getColumnModel().getColumn(2).setPreferredWidth(8)
    pane = JScrollPane(table)
    pane.setVerticalScrollBarPolicy(ScrollPaneConstants.VERTICAL_SCROLLBAR_ALWAYS)
    self.jplTable.setLayout(BorderLayout())
    self.jplTable.add(pane, BorderLayout.CENTER)
    # Access
    #        jpl1 =  self.jpl1.getComponents()[0]
    #    print "Jpl1 - Value Slider: ", jpl1.getValue()
    #
    #self.tblFields.setModel(model)
    #self.getFieldsToUse()

    ###
    ### Property one record
    ###
    propertyOnerecordreport = self.__layer.getProperty("reportbypoint.onerecordreport")
    if propertyOnerecordreport==None:
      propertyOnerecordreport = False
    self.chkOneRecord.setSelected(propertyOnerecordreport)

    ###
    ### Property format 
    ###
    propertyFormat = self.__layer.getProperty("reportbypoint.typereport")
    if propertyFormat==None:
      propertyFormat = 0
    model = self.cboTypeReport.getModel()
    size = model.getSize()
    for i in range(0, size):
      element = model.getElementAt(i)
      if element.getFormatType()==propertyFormat:
        self.cboTypeReport.setSelectedIndex(i)
    
  def getListModel(self, featureType):
    model = DefaultListModel()
    for attr in featureType:
      model.addElement(attr.getName())
    
    return model
    
  def getLayer(self):
    return self.__layer
      

  def getFieldsToUse(self):
    table =  self.jplTable.getComponents()[0].getComponents()[0].getComponents()[0]
    data = table.getModel().getDataVector()
    return data

  def btnTest_click(self,*args):
    self.save()
    print self.__layer.getProperty("reportbypoint.tablenametouse")
    print self.__layer.getProperty("reportbypoint.fields")
    print self.__layer.getProperty("reportbypoint.onerecordreport")
    print self.__layer.getProperty("reportbypoint.typereport")
    
    propertyFormat = self.__layer.getProperty("reportbypoint.typereport")
    if propertyFormat==None:
      propertyFormat = 0
    model = self.cboTypeReport.getModel()
    size = model.getSize()
    print "property format:", size
    for i in range(0, size):
      element = model.getElementAt(i)
      if element.getFormatType()==propertyFormat:
        self.cboTypeReport.setSelectedIndex(i)
    
  def save(self):
    if self.__layer==None:
        return
    self.__layer.setProperty(
      "reportbypoint.tablenametouse",
      self.txtTableNameToUse.getText()
    )
    self.__layer.setProperty(
      "reportbypoint.fields",
      self.getFieldsToUse()
    )
    self.__layer.setProperty(
        "reportbypoint.onerecordreport",
        self.chkOneRecord.isSelected()
    )
    self.__layer.setProperty(
        "reportbypoint.typereport",
        self.cboTypeReport.getSelectedItem().getFormatType()
    )
      
    
def main(*args):
  viewDoc = gvsig.currentView()
  layer = viewDoc.getLayer("manzanas_pob")
  layer = gvsig.currentLayer()
  panel = ReportByPointPanel(layer)
  panel.setPreferredSize(400,300)

  winmgr = ToolsSwingLocator.getWindowManager()
  dialog = winmgr.createDialog(
    panel.asJComponent(),
    "ReportByPoint test",
    "ReportByPoint information",
    winmgr.BUTTONS_OK_CANCEL
  )
  dialog.show(winmgr.MODE.DIALOG)
  if dialog.getAction()==winmgr.BUTTON_OK:
    panel.save()
    print "Ok"
    print "Show field: "
  else:
    print "Cancel"
  