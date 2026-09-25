# Attribute Table to CSV — QGIS Plugin

![logo](logo.png)

**Author:** Mohamed Taily Bah

Exports the attribute table of any loaded vector layer (shapefile, GeoPackage,
etc.) to a CSV file, with optional "selected features only" and an optional
WKT geometry column.

## Install (manual, for testing/development)

1. Find your QGIS profile's plugin folder:
   - **Windows:** `C:\Users\<you>\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\`
   - **macOS:** `~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/`
   - **Linux:** `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/`
2. Copy this whole `attribute_csv_exporter` folder into that plugins directory.
3. Restart QGIS (or use the *Plugin Reloader* plugin during development).
4. Go to **Plugins → Manage and Install Plugins → Installed**, and enable
   "Attribute Table to CSV".
5. A new toolbar button / entry under the **Attribute Table to CSV** menu will
   appear.

## Usage

1. Load your shapefile (or any vector layer) into QGIS as usual
   (`Layer → Add Layer → Add Vector Layer`).
2. Click the plugin's toolbar icon (or menu entry).
3. Pick the layer, choose where to save the `.csv` file, optionally check
   "Export selected features only" or "Include geometry as WKT column".
4. Click OK.

## Notes / possible extensions

- This exports **all fields** in the layer. If you want a field picker
  (checkboxes to include/exclude specific columns), that's a small addition
  to `csv_exporter_dialog.py` — say the word and I'll add it.
- If you'd rather package this as a proper installable `.zip` for the QGIS
  Plugin Manager ("Install from ZIP"), just zip the `attribute_csv_exporter`
  folder itself (not its contents) — see `metadata.txt` for the version info
  QGIS reads.
- For very large layers, consider `layer.getFeatures(QgsFeatureRequest())`
  with a filter/field subset request to speed things up — currently it reads
  every field for every feature.
