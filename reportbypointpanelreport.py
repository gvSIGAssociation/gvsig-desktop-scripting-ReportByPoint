# encoding: utf-8

import gvsig

from gvsig.libs.formpanel import FormPanel

class ReportByPointPanelReport(FormPanel):
    def __init__(self):
        FormPanel.__init__(self, gvsig.getResource(__file__, "reportbypointpanelreport.xml"))
        self.txpReport.setContentType("text/html")

    def setHTMLText(self, text):
        self.txpReport.setText(text)

def main(*args):
    l = ReportByPointPanelReport()
    l.showTool("ReportByPointPanelReport")
    pass