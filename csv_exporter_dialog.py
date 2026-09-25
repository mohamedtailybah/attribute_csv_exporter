import csv
import os

from qgis.core import QgsProject, QgsMapLayer, QgsMessageLog, Qgis
from qgis.gui import QgsFileWidget
from qgis.PyQt.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QComboBox,
    QCheckBox,
    QDialogButtonBox,
    QMessageBox,
    QLabel,
)


class AttributeCsvExporterDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Export Attributes to CSV")
        self.setMinimumWidth(420)

        self.layer_combo = QComboBox(self)
        self.file_widget = QgsFileWidget(self)
        self.file_widget.setStorageMode(QgsFileWidget.SaveFile)
        self.file_widget.setFilter("CSV files (*.csv)")

        self.selected_only_checkbox = QCheckBox(
            "Export selected features only", self
        )
        self.include_geometry_checkbox = QCheckBox(
            "Include geometry as WKT column", self
        )

        form = QFormLayout()
        form.addRow(QLabel("Vector layer:"), self.layer_combo)
        form.addRow(QLabel("Output CSV file:"), self.file_widget)
        form.addRow(self.selected_only_checkbox)
        form.addRow(self.include_geometry_checkbox)

        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self
        )
        button_box.accepted.connect(self.on_accept)
        button_box.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(button_box)
        self.setLayout(layout)

    def refresh_layers(self):
        """Repopulate the layer combo box with currently loaded vector layers."""
        self.layer_combo.clear()
        for layer in QgsProject.instance().mapLayers().values():
            if layer.type() == QgsMapLayer.VectorLayer:
                self.layer_combo.addItem(layer.name(), layer)

    def on_accept(self):
        layer = self.layer_combo.currentData()
        output_path = self.file_widget.filePath()

        if layer is None:
            QMessageBox.warning(self, "No layer", "Please select a vector layer.")
            return
        if not output_path:
            QMessageBox.warning(
                self, "No output file", "Please choose an output CSV file."
            )
            return
        if not output_path.lower().endswith(".csv"):
            output_path += ".csv"

        selected_only = self.selected_only_checkbox.isChecked()
        include_geometry = self.include_geometry_checkbox.isChecked()

        if selected_only and layer.selectedFeatureCount() == 0:
            QMessageBox.warning(
                self,
                "No selection",
                "'Export selected features only' is checked, but no features "
                "are selected on this layer.",
            )
            return

        try:
            count = export_layer_to_csv(
                layer, output_path, selected_only, include_geometry
            )
        except OSError as e:
            QMessageBox.critical(
                self, "Export failed", f"Could not write file:\n{e}"
            )
            return
        except Exception as e:
            QMessageBox.critical(self, "Export failed", str(e))
            QgsMessageLog.logMessage(str(e), "Attribute Table to CSV", Qgis.Critical)
            return

        QMessageBox.information(
            self,
            "Export complete",
            f"Exported {count} feature(s) to:\n{output_path}",
        )
        self.accept()


def export_layer_to_csv(layer, output_path, selected_only=False, include_geometry=False):
    """Write a vector layer's attribute table to a CSV file.

    :param layer: QgsVectorLayer to export.
    :param output_path: destination .csv path.
    :param selected_only: if True, export only currently selected features.
    :param include_geometry: if True, append a WKT geometry column.
    :returns: number of rows written.
    """
    fields = layer.fields()
    field_names = [f.name() for f in fields]
    if include_geometry:
        field_names = field_names + ["WKT"]

    features = layer.selectedFeatures() if selected_only else layer.getFeatures()

    # Make sure the destination folder exists.
    out_dir = os.path.dirname(output_path)
    if out_dir and not os.path.isdir(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    count = 0
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(field_names)
        for feature in features:
            row = list(feature.attributes())
            if include_geometry:
                geom = feature.geometry()
                row.append(geom.asWkt() if geom is not None else "")
            writer.writerow(row)
            count += 1

    return count
