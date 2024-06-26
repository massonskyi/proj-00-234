from typing import List


def save_to_word(data: List, textboxes: List, result_data: List[List[str]]) -> [bool, Exception]:
    """
    Save to word data
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

    # Adding main data table
    table_main = document.add_table(rows=1, cols=3)
    # Fill main data table
    for i, item in enumerate(data_ptr):
        row_cells_main = table_main.add_row().cells
        row_cells_main[0].text = item.get("idx", "")
        row_cells_main[1].text = item.get("name", "")

        # Get text from corresponding QLineEdit in textboxes list
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
        document.save('Untitled.docx')
    except Exception as e:
        return False, Exception(e)
    else:
        return True, None


def save_to_excel(data: List, textboxes: List) -> [bool, Exception]:
    """
    Save data to excel file
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

    data: List = [{'№ п/п': item.get("№ п/п", ""), 'Показатель': item.get("Показатель", ""),
                   'Ответ субъекта': textboxes_ptr[i].text()} for i, item in enumerate(data_prt)]

    df: pd.DataFrame = pd.DataFrame(data)
    try:
        df.to_excel('Untitled.xlsx', index=False)
    except Exception as e:
        return False, Exception(e)
    else:
        return True, None


def save_to_pdf(data: List, textboxes: List) -> [bool, Exception]:
    """
    Save data to pdf file
    :param data: Data to save to pdf file
    :param textboxes: Text boxes to save to pdf file
    :return: True on success, False on failure + Exception
    """
    try:
        from fpdf import FPDF
    except ImportError:
        return False, Exception('FPDF is not installed')

    data_prt: dict | None = data[0].get('mdth', None)
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

    pdf: PDF = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Data from Textboxes", ln=True, align='C')

    for i, item in enumerate(data_prt):
        text: str = f"{item.get('№ п/п', '')} | {item.get('Показатель', '')} | {textboxes_ptr[i].text()}"
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, txt=text.encode('latin-1', 'replace').decode('latin-1'))

    try:
        pdf.output("output.pdf")
    except Exception as e:
        return False, Exception(e)
    else:
        return True, None


def save_to_csv(data: List, textboxes: List) -> [bool, Exception]:
    """
    Save data to csv file with csv format
    :param data: Data to save to csv file with csv format
    :param textboxes: Text boxes to save to csv file with csv format
    :return: True on success, False on failure  + Exception
    """
    try:
        import csv
    except ImportError:
        return False, Exception('CSV is not installed')

    data_prt: dict | None = data[0].get('mdth', None)
    if not data_prt:
        return False, Exception('Data cannot be empty')

    textboxes_ptr: List = textboxes
    if not textboxes_ptr:
        return False, Exception('Text boxes cannot be empty')

    file = None
    try:
        file = open('output.csv', mode='w', newline='', encoding='utf-8')
    except Exception as e:
        return False, Exception(e)
    else:
        writer: csv.writer = csv.writer(file)
        writer.writerow(['№ п/п', 'Показатель', 'Ответ субъекта'])
        try:
            for i, item in enumerate(data_prt):
                writer.writerow([item.get("№ п/п", ""), item.get("Показатель", ""), textboxes_ptr[i].text()])
        except Exception as e:
            return False, Exception(e)
        else:
            return True, None
    finally:
        if file:
            file.close()


def save_to_txt(data: List, textboxes: List) -> [bool, Exception]:
    """
    Save data to txt file
    :param data: Data to save to txt file
    :param textboxes: Text boxes to save to txt file
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
        file = open('output.txt', mode='w', encoding='utf-8')
    except Exception as e:
        return False, Exception(e)
    else:
        for i, item in enumerate(data_prt):
            line = (f"№ п/п: {item.get('№ п/п', '')}, "
                    f"Показатель: {item.get('Показатель', '')}, "
                    f"Ответ субъекта: {textboxes[i].text()}\n")
            try:
                file.write(line)
            except Exception as e:
                return False, Exception(e)
        else:
            return True, None
    finally:
        if file:
            file.close()


def save_to_xml(data: List, textboxes: List) -> [bool, Exception]:
    """
    Save data to xml file
    :param data: Data to save to xml file
    :param textboxes: Text boxes to save to xml file
    :return: True on success, False on failure  + Exception
    """
    try:
        from xml.etree.ElementTree import Element, SubElement, ElementTree
    except ImportError:
        return False, Exception('XML is not installed')

    data_prt: dict | None = data[0].get('mdth', None)
    if not data_prt:
        return False, Exception('Data cannot be empty')

    textboxes_ptr: List = textboxes
    if not textboxes_ptr:
        return False, Exception('Text boxes cannot be empty')

    root: Element = Element('root')
    data: SubElement = SubElement(root, 'data')

    for i, item in enumerate(data_prt):
        entry: SubElement = SubElement(data, 'entry')
        SubElement(entry, 'number').text = item.get('№ п/п', '')
        SubElement(entry, 'indicator').text = item.get('Показатель', '')
        SubElement(entry, 'answer').text = textboxes_ptr[i].text()

    tree: ElementTree = ElementTree(root)
    try:
        tree.write('output.xml', encoding='utf-8', xml_declaration=True)
    except Exception as e:
        return False, Exception(e)
    else:
        return True, None


def save_to_json(data: List, textboxes: List) -> [bool, Exception]:
    """
    Save data to json file with json format
    :param data: Data to save to json file with json format
    :param textboxes: Text boxes to save to json file with json format
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

    data: List = [{'№ п/п': item.get("№ п/п", ""), 'Показатель': item.get("Показатель", ""),
                   'Ответ субъекта': textboxes_ptr[i].text()} for i, item in enumerate(data_prt)]

    file = None
    try:
        file = open('output.json', mode='w', encoding='utf-8')
    except Exception as e:
        return False, Exception(e)
    else:
        try:
            json.dump(data, file, indent=4, ensure_ascii=False)
        except Exception as e:
            return False, Exception(e)
        else:
            return True, None
    finally:
        if file:
            file.close()


def save_to_html(data: List, textboxes: List) -> [bool, Exception]:
    """
    Save data to html file with html format with html format
    :param data: Data to save to html file with html format
    :param textboxes: Text boxes to save to html file with html format
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

    data: List = [{'№ п/п': item.get("№ п/п", ""), 'Показатель': item.get("Показатель", ""),
                   'Ответ субъекта': textboxes_ptr[i].text()} for i, item in enumerate(data_prt)]

    df: pd.DataFrame = pd.DataFrame(data)
    try:
        df.to_html('output.html', index=False)
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

    file = None
    try:
        file = open(filename, mode, encoding=encoding)
    except Exception as e:
        return False, Exception(e)
    else:
        json.dump(data, file, ensure_ascii=False, indent=4)
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
