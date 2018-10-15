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
    i18n = ToolsSwingLocator.getToolsSwingManager()
    i18n.translate(self.lblTableNameToUse)
    i18n.translate(self.lblFields)
    i18n.translate(self.chkOneRecord)
    i18n.translate(self.lblTypeOfReport)
    
    self.setLayer(layer)

    self.cboTypeReport.removeAllItems()
    self.cboTypeReport.addItem("_By_table")
    self.cboTypeReport.addItem("_With_two_columns")

      
  def setLayer(self, layer):
    self.__layer = layer
    self.txtTableNameToUse.setText(self.__layer.getName())
    
    columnNames = ["_Field_name", "_Name_to_show","_Show"]

    # TODO load
    featureType = self.__layer.getFeatureStore().getDefaultFeatureType()
    data = [[attr.getName(), attr.getName(), True] for attr in featureType]

    model = DefaultTableModel(data, columnNames)

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
    self.getFieldsToUse()
      
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
        self.cboTypeReport.getSelectedItem()
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
  