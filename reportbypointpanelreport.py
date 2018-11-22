# encoding: utf-8

import gvsig

from gvsig.libs.formpanel import FormPanel
from org.gvsig.tools.swing.api import ToolsSwingLocator

from java.awt import BorderLayout
from javax.swing import JScrollPane
from javax.swing import JTextPane
from javax.swing import ScrollPaneConstants

class ReportByPointPanelReport(FormPanel):
    def __init__(self):
        FormPanel.__init__(self, gvsig.getResource(__file__, "reportbypointpanelreport.xml"))
        i18Swing = ToolsSwingLocator.getToolsSwingManager()
        self.setPreferredSize(400,300)
        i18Swing.translate(self.lblReport)
        self.txt = JTextPane()
        i18Swing.setDefaultPopupMenu(self.txt)
        self.txt.setContentType("text/html")
        self.pane = JScrollPane(self.txt)
        self.setInitHorizontalScroll()
        self.pane.setVerticalScrollBarPolicy(ScrollPaneConstants.VERTICAL_SCROLLBAR_ALWAYS)
        self.setInitHorizontalScroll()
        #self.pane.setHorizontalScrollBarPolicy(ScrollPaneConstants.HORIZONTAL_SCROLLBAR_ALWAYS)
        self.setInitHorizontalScroll()
        self.jplReport.setLayout(BorderLayout())
        self.jplReport.add(self.pane, BorderLayout.CENTER)
        self.setInitHorizontalScroll()
    def setHTMLText(self, text):
        self.txt.setText(text)
        self.setInitHorizontalScroll()
        
    def setInitHorizontalScroll(self):
        self.pane.getHorizontalScrollBar().setValue(0)


def main(*args):
    l = ReportByPointPanelReport()
    l.showTool("ReportByPointPanelReport")
    l.setHTMLText("""
    <html>
<body>
<p> Reporte para el punto POINT (-95.06769717097485 34.464088096768094) </p><p>TM_WORLD_BORDERS-0.3</p><table style="width:100%"><tr><th>FIPS</th><th>ISO2</th><th>ISO3</th><th>UN</th><th>NAME</th><th>AREA</th><th>POP2005</th><th>REGION</th><th>SUBREGION</th><th>LON</th><th>LAT</th><th>GEOMETRY</th></tr><tr><th>US</th><th>US</th><th>USA</th><th>840</th><th>United States</th><th>915896</th><th>299846449</th><th>19</th><th>21</th><th>-98.606</th><th>39.622</th><th>MultiPolygon:2D</th></tr></table></body>
</html>
     """)
    #l.setInitHorizontalScroll()

    pass