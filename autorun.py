# encoding: utf-8

import gvsig
from gvsig import getResource

from addons.ReportByPoint import actions
from addons.ReportByPoint import reportbypointpropertypage

from org.gvsig.tools import ToolsLocator
from java.io import File

def main(*args):
  i18nManager = ToolsLocator.getI18nManager()
  i18nManager.addResourceFamily("text",File(getResource(__file__,"i18n")))
  
  actions.selfRegister()
  reportbypointpropertypage.selfRegister()
    