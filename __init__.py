def classFactory(iface):
    """Load AttributeCsvExporter class from file csv_exporter_plugin.py.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    from .csv_exporter_plugin import AttributeCsvExporter
    return AttributeCsvExporter(iface)
