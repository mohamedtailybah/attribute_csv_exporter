import os

from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.QtGui import QIcon

from .csv_exporter_dialog import AttributeCsvExporterDialog


class AttributeCsvExporter:
    """QGIS Plugin: export a vector layer's attribute table to CSV."""

    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.actions = []
        self.menu = "&Attribute Table to CSV"
        self.toolbar = self.iface.addToolBar("Attribute Table to CSV")
        self.toolbar.setObjectName("AttributeCsvExporterToolbar")
        self.dlg = None

    def initGui(self):
        icon_path = os.path.join(self.plugin_dir, "icon.png")
        icon = QIcon(icon_path) if os.path.exists(icon_path) else QIcon()

        action = QAction(icon, "Export Attributes to CSV", self.iface.mainWindow())
        action.triggered.connect(self.run)
        action.setEnabled(True)

        self.toolbar.addAction(action)
        self.iface.addPluginToMenu(self.menu, action)
        self.actions.append(action)

    def unload(self):
        for action in self.actions:
            self.iface.removePluginMenu(self.menu, action)
            self.iface.removeToolBarIcon(action)
        del self.toolbar

    def run(self):
        if self.dlg is None:
            self.dlg = AttributeCsvExporterDialog(self.iface.mainWindow())
        self.dlg.refresh_layers()
        self.dlg.show()
        self.dlg.exec_()
