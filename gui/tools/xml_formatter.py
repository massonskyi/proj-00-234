from PySide6.QtWidgets import QTextEdit
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString


class XmlFormatter:
    @classmethod
    def format_xml(cls, text_edit: QTextEdit, text: str):
        try:
            tree = ET.ElementTree(ET.fromstring(text))

            xml_str = ET.tostring(tree.getroot(), encoding='unicode')

            dom = parseString(xml_str)
            formatted_xml = dom.toprettyxml(indent="    ")

            text_edit.clear()
            text_edit.append(formatted_xml)

        except ET.ParseError as e:
            text_edit.clear()
            text_edit.append(f"Invalid XML: {str(e)}")
