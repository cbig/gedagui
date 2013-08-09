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
                          pyqtSlot, Qt)
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

        self.actionGet_selected.setEnabled(False)

        self.file_treeView.doubleClicked.connect(self.update_selected)
        self.file_treeView.doubleClicked.connect(self.update_controls)

        # Dict to hold the actual paths to selected zips
        self.selected = {}

        # Location where the files are to be downloaded
        self.destination = ""

    @pyqtSlot()
    def on_actionAbout_triggered(self):
        QMessageBox.about(self, "About gedaGUI",
                          """<b>Global Environmental Decision Analysis GUI</b>
                            <p>Copyright &copy; 2011 Joona Lehtomaki
                            <joona.lehtomaki@gmail.com>. \n
                            All rights reserved, released under MIT license.
                            <p>Support for GEDA project.</p>
                            <p>Python %s - Qt %s - PyQt %s on %s</p>""" % (VERSION, platform.python_version(),
                                                                           QT_VERSION,
                                                                           PYQT_VERSION, platform.system()))

    @pyqtSlot()
    def on_actionGet_selected_triggered(self):
        pass

    @pyqtSlot()
    def on_actionOpen_location_triggered(self):
        # Get the locations
        path = QFileDialog.getExistingDirectory(self, 'Open location', '~')
        if path:
            self.update_dirmodel(path)

    @pyqtSlot()
    def on_removeSelected_pushButton_clicked(self):
        pass

    @pyqtSlot()
    def on_setDestination_toolButton_clicked(self):
        path = QFileDialog.getExistingDirectory(self, 'Set destination', '~')
        self.path_lineEdit.setText(path)
        self.destination = path
        self.update_controls()

    def update_controls(self):
        if self.selected_listWidget.count() > 0:
            # FIXME: this should only be enabled if there are selected items
            self.removeSelected_pushButton.setEnabled(True)
            if self.destination != "":
                self.actionGet_selected.setEnabled(True)
                self.getSelected_pushButton.setEnabled(True)
        else:
            self.removeSelected_pushButton.setEnabled(False)
            self.actionGet_selected.setEnabled(False)
            self.getSelected_pushButton.setEnabled(False)

    def update_dirmodel(self, path):
        dirmodel = QFileSystemModel()
        dirmodel.setFilter(QDir.NoDotAndDotDot | QDir.AllEntries)
        filefilter = ["*.zip"]
        dirmodel.setNameFilters(filefilter)
        self.file_treeView.setModel(dirmodel)
        self.file_treeView.header().setResizeMode(3)
        self.file_treeView.model().setRootPath(path)
        self.file_treeView.setRootIndex(self.file_treeView.model().index(path))

    def update_selected(self, index):
        fileinfo = self.file_treeView.model().fileInfo(index)
        filename = fileinfo.fileName()
        all_items = self.selected_listWidget.findItems(filename, Qt.MatchRegExp)
        if not all_items and filename.endsWith('zip'):
            self.selected_listWidget.addItem(fileinfo.fileName())
            print(fileinfo.filePath())
            self.selected[filename] = fileinfo.filePath()

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
