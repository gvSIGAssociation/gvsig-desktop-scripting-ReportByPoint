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
        pane = JScrollPane(self.txt)
        pane.setVerticalScrollBarPolicy(ScrollPaneConstants.VERTICAL_SCROLLBAR_ALWAYS)
        pane.setHorizontalScrollBarPolicy(ScrollPaneConstants.HORIZONTAL_SCROLLBAR_AS_NEEDED)
        self.jplReport.setLayout(BorderLayout())
        self.jplReport.add(pane, BorderLayout.CENTER)
    def setHTMLText(self, text):
        self.txt.setText(text)

def main(*args):
    l = ReportByPointPanelReport()
    l.showTool("ReportByPointPanelReport")
    l.setHTMLText("""
<table style="width:100%">
  <tr>
    <th>Firstname</th>
    <th>Lastname</th> 
    <th>Age</th>
  </tr>
  <tr>
    <td>Jill</td>
    <td>Smith</td> 
    <td>50</td>
  </tr>
  <tr>
    <td>Eve</td>
    <td>Jackson</td> 
    <td>94</td>
  </tr>
</table><table style="width:100%">
  <tr>
    <th>Firstname</th>
    <th>Lastname</th> 
    <th>Age</th>
  </tr>
  <tr>
    <td>Jill</td>
    <td>Smith</td> 
    <td>50</td>
  </tr>
  <tr>
    <td>Eve</td>
    <td>Jackson</td> 
    <td>94</td>
  </tr>
</table><table style="width:100%">
  <tr>
    <th>Firstname</th>
    <th>Lastname</th> 
    <th>Age</th>
  </tr>
  <tr>
    <td>Jill</td>
    <td>Smith</td> 
    <td>50</td>
  </tr>
  <tr>
    <td>Eve</td>
    <td>Jackson</td> 
    <td>94</td>
  </tr>
</table><table style="width:100%">
  <tr>
    <th>Firstname</th>
    <th>Lastname</th> 
    <th>Age</th>
  </tr>
  <tr>
    <td>Jill</td>
    <td>Smith</td> 
    <td>50</td>
  </tr>
  <tr>
    <td>Eve</td>
    <td>Jackson</td> 
    <td>94</td>
  </tr>
</table><table style="width:100%">
  <tr>
    <th>Firstname</th>
    <th>Lastname</th> 
    <th>Age</th>
  </tr>
  <tr>
    <td>Jill</td>
    <td>Smith</td> 
    <td>50</td>
  </tr>
  <tr>
    <td>Eve</td>
    <td>Jackson</td> 
    <td>94</td>
  </tr>
</table><table style="width:100%">
  <tr>
    <th>Firstname</th>
    <th>Lastname</th> 
    <th>Age</th>
  </tr>
  <tr>
    <td>Jill</td>
    <td>Smith</td> 
    <td>50</td>
  </tr>
  <tr>
    <td>Eve</td>
    <td>Jackson</td> 
    <td>94</td>
  </tr>
</table>
     """)

    pass