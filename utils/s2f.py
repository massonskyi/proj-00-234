from typing import List


def save_to_word(path: str, data: List, textboxes: List, result_data: List[List[str]]) -> [bool, Exception]:
    """
    Save to word data
    :param path: path to save to file
    :param result_data: Data to save to word file
    :param data: Data to save to word file
    :param textboxes: Text boxes to save to word file
    :return: True on success, False on failure + Exception
    """
    try:
        from docx import Document
    except ImportError:
        return False, Exception('docx module is not installed')

    data_ptr: dict | None = data[0].get('mdth', None)
    if not data_ptr:
        return False, Exception('Data cannot be empty')

    textboxes_ptr: List = textboxes
    if not textboxes_ptr:
        return False, Exception('Text boxes cannot be empty')

    document = Document()
    document.add_heading("РЕЗУЛЬТАТЫ", level=1)

    table_main = document.add_table(rows=1, cols=3)

    for i, item in enumerate(data_ptr):
        row_cells_main = table_main.add_row().cells
        row_cells_main[0].text = item.get("idx", "")
        row_cells_main[1].text = item.get("name", "")

        if i < len(textboxes):
            row_cells_main[2].text = textboxes[i].text()

    if result_data:
        document.add_paragraph("\n")
        document.add_heading("Таблица результатов", level=2)

        table_results = document.add_table(rows=len(result_data), cols=len(result_data[0]) if result_data else 0)
        for row, row_data in enumerate(result_data):
            for col, value in enumerate(row_data):
                cell = table_results.cell(row, col)
                cell.text = str(value)
    try:
        document.save(f'{path}/export/Untitled.docx')
    except Exception as e:
        return False, Exception(e)
    else:
        return True, None


def save_to_excel(path: str, data: List, textboxes: List, result_data: List[List[str]]) -> [bool, Exception]:
    """
    Save data to excel file
    :param path: path to save to file
    :param data: Data to save to excel file
    :param textboxes: Text boxes to save to excel file
    :return: True on success, False on failure + Exception
    """
    try:
        import pandas as pd
    except ImportError:
        return False, Exception('Pandas is not installed')

    data_prt: dict | None = data[0].get('mdth', None)
    if not data_prt:
        return False, Exception('Data cannot be empty')

    textboxes_ptr: List = textboxes
    if not textboxes_ptr:
        return False, Exception('Text boxes cannot be empty')

    data_list: List = [{'№ п/п': item.get("idx", ""), 'Показатель': item.get("name", ""),
                        'data': textboxes_ptr[i].text()} for i, item in enumerate(data_prt)]
    try:
        df_data = pd.DataFrame(data_list)
        df_result = pd.DataFrame(result_data) if result_data else None
    except Exception as e:
        return False, Exception(e)
    else:
        try:
            with pd.ExcelWriter(f'{path}/export/Untitled.xlsx') as writer:
                df_data.to_excel(writer, sheet_name='Data', index=False)
                if df_result is not None:
                    df_result.to_excel(writer, sheet_name='Result Data', index=False)
        except Exception as e:
            return False, Exception(e)
        else:
            return True, None


def save_to_pdf(path: str, data: List, textboxes: List, result_data: List[List[str]]) -> [bool, Exception]:
    """
    Save data to pdf file
    :param path: path to save to file
    :param data: Data to save to pdf file
    :param textboxes: Text boxes to save to pdf file
    :param result_data: Result data to save to pdf file
    :return: True on success, False on failure + Exception
    """
    try:
        from fpdf import FPDF
    except ImportError:
        return False, Exception('FPDF is not installed')

    data_prt = data[0].get('mdth', None)
    if not data_prt:
        return False, Exception('Data cannot be empty')

    textboxes_ptr: List = textboxes
    if not textboxes_ptr:
        return False, Exception('Text boxes cannot be empty')

    class PDF(FPDF):
        """
        PDF class for saving data to pdf file
        """

        def header(self) -> None:
            """
            Set header of pdf file
            :return: None
            """
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, 'Data from Textboxes', 0, 1, 'C')

    pdf = PDF()
    pdf.add_page()

    font_path = './fonts/DejaVuSans.ttf'
    bold_dejavu_path = './fonts/DejaVuSansBold.ttf'

    pdf.add_font('DejaVu', '', font_path, uni=True)
    pdf.add_font('DejaVu-Bold', '', bold_dejavu_path, uni=True)
    pdf.set_font('DejaVu-Bold', '', 12)

    pdf.cell(200, 10, txt="Data from Textboxes", ln=True, align='C')

    for i, item in enumerate(data_prt):
        text = f"{item.get('idx', '')} | {item.get('name', '')} | {textboxes_ptr[i].text()}"
        pdf.set_font('DejaVu', '', 12)
        pdf.multi_cell(0, 10, txt=text)

    pdf.add_page()
    pdf.set_font('DejaVu-Bold', '', 12)
    pdf.cell(200, 10, txt="Result Data", ln=True, align='C')

    for row in result_data:
        text = " | ".join(row)
        pdf.set_font('DejaVu', '', 12)
        pdf.multi_cell(0, 10, txt=text)

    try:
        pdf.output(f'{path}/export/Untitled.pdf')
    except Exception as e:
        return False, Exception(e)
    else:
        return True, None


def save_to_csv(path: str, data: List, textboxes: List, result_data: List[List[str]]) -> [bool, Exception]:
    """
    Save data to csv file with csv format
    :param path: path to save to file
    :param data: Data to save to csv file with csv format
    :param textboxes: Text boxes to save to csv file with csv format
    :param result_data: Result data to save to csv file
    :return: True on success, False on failure + Exception
    """
    try:
        import csv
    except ImportError:
        return False, Exception('CSV module is not installed')

    data_prt = data[0].get('mdth', None)
    if not data_prt:
        return False, Exception('Data cannot be empty')

    textboxes_ptr: List = textboxes
    if not textboxes_ptr:
        return False, Exception('Text boxes cannot be empty')

    file = None
    try:
        file = open(f"{path}/export/Untitled.csv", mode='w', newline='', encoding='utf-8')
        writer = csv.writer(file)

        writer.writerow(['№ п/п', 'Показатель', 'Ответ субъекта'])
        for i, item in enumerate(data_prt):
            writer.writerow([item.get("idx", ""), item.get("name", ""), textboxes_ptr[i].text()])

        writer.writerow([])

        writer.writerow(['Result Data'])
        for row in result_data:
            writer.writerow(row)

    except Exception as e:
        return False, Exception(e)
    else:
        return True, None
    finally:
        if file:
            file.close()


def save_to_txt(path: str, data: List, textboxes: List, result_data: List[List[str]]) -> [bool, Exception]:
    """
    Save data to txt file
    :param path: path to save to file
    :param data: Data to save to txt file
    :param textboxes: Text boxes to save to txt file
    :param result_data: Result data to save to txt file
    :return: True on success, False on failure + Exception
    """
    data_prt: dict | None = data[0].get('mdth', None)
    if not data_prt:
        return False, Exception('Data cannot be empty')

    textboxes_ptr: List = textboxes
    if not textboxes_ptr:
        return False, Exception('Text boxes cannot be empty')

    file = None
    try:
        file = open(f'{path}/export/Untitled.txt', mode='w', encoding='utf-8')
    except Exception as e:
        return False, Exception(e)
    else:
        for i, item in enumerate(data_prt):
            line = (f"№ п/п: {item.get('idx', '')}, "
                    f"Показатель: {item.get('name', '')}, "
                    f"Ответ субъекта: {textboxes[i].text()}\n")
            try:
                file.write(line)
            except Exception as e:
                return False, Exception(e)

        file.write("\n")
        if result_data:
            file.write("Result Data:\n")

            for row in result_data:
                line = " | ".join(row) + "\n"

                try:
                    file.write(line)
                except Exception as e:
                    return False, Exception(e)

        else:
            return True, None
    finally:
        if file:
            file.close()


def save_to_xml(path: str, data: List, textboxes: List, result_data: List[List[str]]) -> [bool, Exception]:
    """
    Save data and result_data to xml file
    :param path: path to save to file
    :param data: Data to save to xml file
    :param textboxes: Text boxes to save to xml file
    :param result_data: Result data to save to xml file
    :return: True on success, False on failure + Exception
    """
    try:
        from xml.etree.ElementTree import Element, SubElement, ElementTree
    except ImportError:
        return False, Exception('XML is not installed')

    data_prt = data[0].get('mdth', None)
    if not data_prt:
        return False, Exception('Data cannot be empty')

    textboxes_ptr: List = textboxes
    if not textboxes_ptr:
        return False, Exception('Text boxes cannot be empty')

    root = Element('root')

    data_element = SubElement(root, 'data')
    for i, item in enumerate(data_prt):
        entry = SubElement(data_element, 'entry')
        SubElement(entry, 'number').text = item.get('idx', '')
        SubElement(entry, 'indicator').text = item.get('name', '')
        SubElement(entry, 'answer').text = textboxes_ptr[i].text()

    if result_data:
        result_element = SubElement(root, 'result_data')
        for row in result_data:
            entry = SubElement(result_element, 'entry')
            SubElement(entry, 'field1').text = row[0] if len(row) > 0 else ''
            SubElement(entry, 'field2').text = row[1] if len(row) > 1 else ''
            SubElement(entry, 'field3').text = row[2] if len(row) > 2 else ''

    tree = ElementTree(root)
    try:
        tree.write(f'{path}/export/Untitled.xml', encoding='utf-8', xml_declaration=True)
    except Exception as e:
        return False, Exception(e)
    else:
        return True, None


def save_to_json(path: str, data: List, textboxes: List, result_data: List[List[str]]) -> [bool, Exception]:
    """
    Save data to json file with json format
    :param path: path to save to file
    :param data: Data to save to json file with json format
    :param textboxes: Text boxes to save to json file with json format
    :param result_data: Result data to save to json file
    :return: True on success, False on failure + Exception
    """
    try:
        import json
    except ImportError:
        return False, Exception('JSON is not installed')

    data_prt: dict | None = data[0].get('mdth', None)
    if not data_prt:
        return False, Exception('Data cannot be empty')

    textboxes_ptr: List = textboxes
    if not textboxes_ptr:
        return False, Exception('Text boxes cannot be empty')

    # Prepare data
    data_list = [{'№ п/п': item.get("idx", ""), 'Показатель': item.get("name", ""),
                  'data': textboxes_ptr[i].text()} for i, item in enumerate(data_prt)]

    result_list = [{'Field1': row[0], 'Field2': row[1], 'Field3': row[2]} for row in result_data] if result_data else []

    combined_data = {'data': data_list, 'result_data': result_list}

    file = None
    try:
        file = open(f'{path}/export/Untitled.json', mode='w', encoding='utf-8')
    except Exception as e:
        return False, Exception(e)
    else:
        try:
            json.dump(combined_data, file, indent=4, ensure_ascii=False)
        except Exception as e:
            return False, Exception(e)
        else:
            return True, None
    finally:
        if file:
            file.close()


def save_to_html(path: str, data: List, textboxes: List, result_data: List[List[str]]) -> [bool, Exception]:
    """
    Save data to html file with html format with html format
    :param path: path to save to file
    :param data: Data to save to html file with html format
    :param textboxes: Text boxes to save to html file with html format
    :param result_data: Result data to save to html file
    :return: True on success, False on failure + Exception
    """
    try:
        import pandas as pd
    except ImportError:
        return False, Exception('Pandas is not installed')

    data_prt: dict | None = data[0].get('mdth', None)
    if not data_prt:
        return False, Exception('Data cannot be empty')

    textboxes_ptr: List = textboxes
    if not textboxes_ptr:
        return False, Exception('Text boxes cannot be empty')

    # Prepare data
    data_list = [{'№ п/п': item.get("idx", ""), 'Показатель': item.get("name", ""),
                  'Ответ субъекта': textboxes_ptr[i].text()} for i, item in enumerate(data_prt)]
    data_df = pd.DataFrame(data_list)
    data_html = data_df.to_html(index=False)
    result_df = pd.DataFrame(result_data) if result_data else pd.DataFrame()
    result_html = result_df.to_html(index=False)
    try:
        with open(f'{path}/export/Untitled.html', mode='w', encoding='utf-8') as file:
            file.write("<html><head><title>Output HTML</title></head><body>\n")
            file.write("<h2>Data from Textboxes</h2>\n")
            file.write(data_html)
            file.write("<h2>Result Data</h2>\n")
            file.write(result_html)
            file.write("</body></html>")
    except Exception as e:
        return False, Exception(e)
    else:
        return True, None


def generate_mdth_file(data, filename: str, mode: str = "w", encoding: str = "utf-8") -> [bool, Exception]:
    """
    Generate markdown file from data
    :param data: data to save
    :param filename: file name to save markdown
    :param mode: (Optional) mode to save file
    :param encoding: (Optional) encoding to save file
    :return: True or False with Exception
    """
    try:
        import json
    except ImportError:
        return False, Exception('JSON is not installed')
    try:
        json_data = json.dumps(data, ensure_ascii=False, indent=4)
    except Exception as e:
        return False, e

    file = None
    try:
        file = open(filename, mode, encoding=encoding)
    except Exception as e:
        return False, Exception(e)
    else:
        file.write(json_data)
        return True, None
    finally:
        if file:
            file.close()


def load_mdth_file(filename: str) -> [bool, Exception]:
    """
    Load markdown file from file
    :param filename:  file name to load
    :return: load markdown
    """
    import json
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            data = json.loads(content)
            return data

    except FileNotFoundError:
        print(f"Файл '{filename}' не найден.")
        return None
    except json.JSONDecodeError as e:
        print(f"Ошибка при чтении файла '{filename}': {e}")
        return None
