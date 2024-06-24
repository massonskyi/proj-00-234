def s2txt(filename: str, text: str, mode: str = "w", encoding: str = "utf-8") -> [bool, Exception]:
    """
    Save text to file
    :param filename: file name to save text
    :param text: text to save
    :param mode: (Optional) mode to save file
    :param encoding: (Optional) encoding to save file
    :return: True or False with Exception
    """
    f = None
    try:
        f = open(filename, mode=mode, encoding=encoding)
    except Exception as e:
        return False, Exception(f"Error saving text to file: {e}")

    else:
        f.write(text)
        f.close()
        return True, None

    finally:
        if f:
            f.close()


def s2json(filename: str, data: dict, mode: str = "w", encoding: str = "utf-8") -> [bool, Exception]:
    """
    Save json to file
    :param filename: file name to save json
    :param data: json to save
    :param mode: (Optional) mode to save file
    :param encoding: (Optional) encoding to save file
    :return: True or False with Exception
    """
    import json
    f = None
    try:
        f = open(filename, mode=mode, encoding=encoding)
    except Exception as e:
        return False, Exception(f"Error saving json to file: {e}")

    else:
        json.dump(data, f)
        f.close()
        return True, None

    finally:
        if f:
            f.close()


def s2csv(filename: str, data: dict, mode: str = "w", encoding: str = "utf-8") -> [bool, Exception]:
    """
    Save csv to file
    :param filename: file name to save csv
    :param data: csv to save
    :param mode: (Optional) mode to save file
    :param encoding: (Optional) encoding to save file
    :return: True or False with Exception
    """
    import csv
    f = None
    try:
        f = open(filename, mode=mode, encoding=encoding)
    except Exception as e:
        return False, Exception(f"Error saving csv to file: {e}")

    else:
        csv_writer = csv.writer(f)
        csv_writer.writerow(data.keys())
        csv_writer.writerow(data.values())
        f.close()
        return True, None

    finally:
        if f:
            f.close()


def s2excel(filename: str, data: dict, mode: str = "w", encoding: str = "utf-8") -> [bool, Exception]:
    """
    Save excel to file
    :param filename: file name to save excel
    :param data: excel to save
    :param mode: (Optional) mode to save file
    :param encoding: (Optional) encoding to save file
    :return: True or False with Exception
    """
    import pandas as pd
    f = None
    try:
        f = open(filename, mode=mode, encoding=encoding)
    except Exception as e:
        return False, Exception(f"Error saving excel to file: {e}")

    else:
        df = pd.DataFrame(data, index=[0])
        df.to_excel(f)
        f.close()
        return True, None

    finally:
        if f:
            f.close()


def s2pdf(filename: str, data: dict, mode: str = "w", encoding: str = "utf-8") -> [bool, Exception]:
    """
    Save pdf to file
    :param filename: file name to save pdf
    :param data: pdf to save
    :param mode: (Optional) mode to save file
    :param encoding: (Optional) encoding to save file
    :return: True or False with Exception
    """
    import pdfkit
    f = None
    try:
        f = open(filename, mode=mode, encoding=encoding)
    except Exception as e:
        return False, Exception(f"Error saving pdf to file: {e}")

    else:
        pdfkit.from_string(data, f)
        f.close()
        return True, None

    finally:
        if f:
            f.close()


def s2html(filename: str, data: dict, mode: str = "w", encoding: str = "utf-8") -> [bool, Exception]:
    """
    Save html to file
    :param filename: file name to save html
    :param data: html to save
    :param mode: (Optional) mode to save html file
    :param encoding: (Optional) encoding to save html file
    :return: True or False with Exception
    """
    f = None
    try:
        f = open(filename, mode=mode, encoding=encoding)
    except Exception as e:
        return False, Exception(f"Error saving html to file: {e}")

    else:
        f.write(data)
        f.close()
        return True, None

    finally:
        if f:
            f.close()


def s2xml(filename: str, data: dict, mode: str = "w", encoding: str = "utf-8") -> [bool, Exception]:
    """
    Save xml to file
    :param filename: file name to save xml
    :param data: xml to save
    :param mode: (Optional) mode to save file
    :param encoding: (Optional) encoding to save file
    :return: True or False with Exception
    """
    f = None
    try:
        f = open(filename, mode=mode, encoding=encoding)
    except Exception as e:
        return False, Exception(f"Error saving xml to file: {e}")

    else:
        f.write(data)
        f.close()
        return True, None

    finally:
        if f:
            f.close()


def s2yaml(filename: str, data: dict, mode: str = "w", encoding: str = "utf-8") -> [bool, Exception]:
    """
    Save yaml to file
    :param filename: file name to save yaml
    :param data: yaml to save
    :param mode: (Optional) mode to save file
    :param encoding: (Optional) encoding to save file
    :return: True or False with Exception
    """
    import yaml
    f = None
    try:
        f = open(filename, mode=mode, encoding=encoding)
    except Exception as e:
        return False, Exception(f"Error saving yaml to file: {e}")

    else:
        yaml.dump(data, f)
        f.close()
        return True, None
    finally:
        if f:
            f.close()