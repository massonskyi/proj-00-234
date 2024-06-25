import os

import docx
import json


def create_configuration_config_mdt():
    """
    Create configuration for MDT
    """

    docx_file = './doc.docx'
    json_file = './configuration_config_mdt.json'

    if not os.path.exists(docx_file):
        raise FileNotFoundError(f'File {docx_file} not found.')

    table_data = read_table_from_docx(docx_file)
    save_as_json(table_data, json_file)

    print(f"Table data extracted from '{docx_file}' and saved as '{json_file}'.")


def read_table_from_docx(docx_file):
    doc = docx.Document(docx_file)
    table = doc.tables[0]  # Assuming the table is the first table in the document

    data = []
    keys = [cell.text.strip() for cell in table.rows[0].cells]  # Assuming the first row as header

    for row in table.rows[1:]:  # Start from the second row for data
        row_data = {}
        for idx, cell in enumerate(row.cells):
            row_data[keys[idx]] = cell.text.strip()
        data.append(row_data)

    return data


def save_as_json(data, json_file):
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    docx_file = '/home/user064/PycharmProjects/proj-00-234/doc.docx'  # Replace with your Word document filename
    json_file = '../configuration_config_mdt.json'  # JSON output filename

    table_data = read_table_from_docx(docx_file)
    save_as_json(table_data, json_file)
    print(f"Table data extracted from '{docx_file}' and saved as '{json_file}'.")
