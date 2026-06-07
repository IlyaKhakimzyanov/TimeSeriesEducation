import json
import random
from pathlib import Path
import xml.etree.ElementTree as ET


def parse_geojson_to_kml(geojson_path: Path, kml_path: Path):
    with open(geojson_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    kml = ET.Element("kml", xmlns="http://www.opengis.net/kml/2.2")
    document = ET.SubElement(kml, "Document")

    for feature in data['features']:
        coords = feature['geometry']['coordinates'][0]
        cell_id = feature['properties']['cellId']

        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)

        placemark = ET.SubElement(document, "Placemark")
        name = ET.SubElement(placemark, "name")
        name.text = str(cell_id)

        style = ET.SubElement(placemark, "Style")
        linestyle = ET.SubElement(style, "LineStyle")
        linecolor = ET.SubElement(linestyle, "color")
        linecolor.text = "ff000000"
        linewidth = ET.SubElement(linestyle, "width")
        linewidth.text = "2"

        polystyle = ET.SubElement(style, "PolyStyle")
        polycolor = ET.SubElement(polystyle, "color")
        polycolor.text = f"66{r:02x}{g:02x}{b:02x}"

        polygon = ET.SubElement(placemark, "Polygon")
        outerboundary = ET.SubElement(polygon, "outerBoundaryIs")
        linearring = ET.SubElement(outerboundary, "LinearRing")
        coordinates = ET.SubElement(linearring, "coordinates")

        coord_text = " ".join([f"{lon},{lat},0" for lon, lat in coords])
        coord_text += f" {coords[0][0]},{coords[0][1]},0"
        coordinates.text = coord_text

    tree = ET.ElementTree(kml)
    tree.write(kml_path, encoding="utf-8", xml_declaration=True)


geojson_file = Path("trentino-grid.geojson")
kml_file = Path("trentino-grid.kml")
parse_geojson_to_kml(geojson_file, kml_file)
