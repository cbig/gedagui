#!/usr/bin/python
# coding=utf-8

import os 
import platform
import sys
from types import BooleanType, FloatType, IntType, ListType, StringType

from PyQt4.QtGui import (QAction, QActionGroup, QColor, QFileDialog, 
                         QFileSystemModel,
                         QMainWindow, QMenu, QMessageBox, QTextCursor, 
                         QTreeWidgetItem)
from PyQt4.QtCore import (QDir, QPoint, QSettings, QSize, QStringList, QVariant, 
                          pyqtSlot)
from PyQt4.QtCore import PYQT_VERSION, QT_VERSION

from gedagui.resources.ui_mainWindow import Ui_MainWindow
from gedagui.utilities import (APP_RESOURCES, USER_DATA_DIR, VERSION)

#------------------------------------------------------------------------------ 
# Main graphical components

class MainWindow(QMainWindow, Ui_MainWindow):
    '''Mainwindow for initial loading of different plugins.
    '''
    
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.statusbar.showMessage("gedaGUI ready", 4000)
        
        
    
    def update_ui(self):
        if self.toolTreeWidget.currentItem():
            self.actionLoad_tool.setEnabled(True)
            selected_tool = str(self.toolTreeWidget.currentItem().text(0))
            help_text = self.manager.plugins[selected_tool].help
            self.helpTextEdit.setText(help_text)
        
        extent = self.extenactiongroup.checkedAction()
        if extent: 
            self.extentLabel.setText("Current extent: %s" % extent.text())
    
    @pyqtSlot()
    def on_actionAbout_triggered(self):
        QMessageBox.about(self, "About gedaGUI",
                          """<b>Global Environmental Decision Analysis GUI</b> v %s
                            <p>Copyright &copy; 2011 Joona Lehtomaki 
                            <joona.lehtomaki@gmail.com>.
                            All rights reserved, released under MIT license.
                            <p>Support for GEDA project.</p>
                            <p>Python %s - Qt %s - PyQt %s on %s</p>""" % (
                            VERSION, platform.python_version(),
                            QT_VERSION,
                            PYQT_VERSION, platform.system()))

    @pyqtSlot()
    def on_actionOpen_location_triggered(self):
        # Get the location 
        path = QFileDialog.getExistingDirectory(self, 'Open location', '~')
        self.path_lineEdit.setText(path)
        self.update_dirmodel(path)
        
        
    def update_dirmodel(self, path):
        dirmodel = QFileSystemModel()
        dirmodel.setFilter(QDir.NoDotAndDotDot | QDir.AllEntries)
        filefilter = ["*.zip"] 
        dirmodel.setNameFilters(filefilter)
        self.file_treeView.setModel(dirmodel)
        self.file_treeView.header().setResizeMode(1)
        self.file_treeView.model().setRootPath(path)
        self.file_treeView.setRootIndex(self.file_treeView.model().index(path))
        
        
        

#------------------------------------------------------------------------------ 
# Run the main GUI

def main():
    
    # Init the Qt basics
    from PyQt4.QtGui import QApplication
    app = QApplication(sys.argv)
    app.setApplicationName("gedaGUI")
    app.setApplicationVersion(VERSION)
    app.setOrganizationName("HU")
    app.setOrganizationDomain("MRG")
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()
    