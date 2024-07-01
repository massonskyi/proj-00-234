import os
import sys
from typing import LiteralString

from PySide6.QtWidgets import QApplication, QMessageBox

from config.cfg import EXE_DIR
from gui.startmenu import Ui_StartMenu
from gui.widgets.start_screen import SplashScreen


def get_resource_path(relative_path) -> LiteralString | str | bytes:
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def configurate_assets() -> dict:
    """
    Configures the application assets.
    :return: dict containing the icons to be used in the application.
    """
    from config.cfg import EXE_DIR
    from utils.loaders import load_icon
    path_to_assets = get_resource_path('assets')

    icons = {
        'hidden_folder': load_icon(get_resource_path(os.path.join('assets', 'folder', 'hidden_folder.png'))),
        'open_clear_folder': load_icon(get_resource_path(os.path.join('assets', 'folder', 'open_clear_folder.png'))),
        'open_full_folder': load_icon(get_resource_path(os.path.join('assets', 'folder', 'open_full_folder.png'))),
        'bash': load_icon(get_resource_path(os.path.join('assets', 'console', 'bash.png'))),
        'py': load_icon(get_resource_path(os.path.join('assets', 'console', 'py.png'))),
        'test_btn': load_icon(get_resource_path(os.path.join('assets', 'test', 'button.png'))),
        'success_question': load_icon(get_resource_path(os.path.join('assets', 'test', 'qs.png'))),
        'failed_question': load_icon(get_resource_path(os.path.join('assets', 'test', 'qc.png'))),
        'process_question': load_icon(get_resource_path(os.path.join('assets', 'folder', 'qp.png'))),
        'menu_exit': load_icon(get_resource_path(os.path.join('assets', 'main', 'menu_exit.png'))),
        'menu_file': load_icon(get_resource_path(os.path.join('assets', 'main', 'menu_file.png'))),
        'menu_new': load_icon(get_resource_path(os.path.join('assets', 'main', 'menu_new.png'))),
        'button': load_icon(get_resource_path(os.path.join('assets', 'default', 'button.png'))),
        'menu_new_file': load_icon(get_resource_path(os.path.join('assets', 'main', 'menu_new_file.png'))),
        'menu_new_project': load_icon(get_resource_path(os.path.join('assets', 'main', 'menu_new_project.png'))),
        'menu_open': load_icon(get_resource_path(os.path.join('assets', 'main', 'menu_open.png'))),
        'menu_open_file': load_icon(get_resource_path(os.path.join('assets', 'main', 'menu_open_file.png'))),
        'menu_open_project': load_icon(get_resource_path(os.path.join('assets', 'main', 'menu_open_project.png'))),
        'menu_save': load_icon(get_resource_path(os.path.join('assets', 'main', 'menu_save.png'))),
        'menu_save_as': load_icon(get_resource_path(os.path.join('assets', 'main', 'menu_save_as.png'))),
        'main_menu': load_icon(get_resource_path(os.path.join('assets', 'main', 'main_menu.png'))),
        'menu_txt': load_icon(get_resource_path(os.path.join('assets', 'main', 'menu_txt.png'))),
        'minimize': load_icon(get_resource_path(os.path.join('assets', 'title', 'minimize.png'))),
        'maximize': load_icon(get_resource_path(os.path.join('assets', 'title', 'maximize.png'))),
        'close': load_icon(get_resource_path(os.path.join('assets', 'title', 'close.png'))),
        'title_main': load_icon(get_resource_path(os.path.join('assets', 'title_main'))),
        'graph': load_icon(get_resource_path(os.path.join('assets', 'folder', 'graph.png'))),
        'bar_chart': load_icon(get_resource_path(os.path.join('assets', 'default', 'bar_chart.png'))),
        'function_f_graph': load_icon(get_resource_path(os.path.join('assets', 'default', 'function_f_graph.png'))),
        'start_screen_pixmap': get_resource_path(os.path.join('assets', 'start_screen.jpg')),
    }
    saves_icons = {
        'save_word': load_icon(get_resource_path(os.path.join('assets', 'save2', 'sword.png'))),
        'save_excel': load_icon(get_resource_path(os.path.join('assets', 'save2', 'sexcel.png'))),
        'save_pdf': load_icon(get_resource_path(os.path.join('assets', 'save2', 'spdf.png'))),
        'save_csv': load_icon(get_resource_path(os.path.join('assets', 'save2', 'scsv.png'))),
        'save_json': load_icon(get_resource_path(os.path.join('assets', 'save2', 'sjson.png'))),
        'save_html': load_icon(get_resource_path(os.path.join('assets', 'save2', 'shtml.png'))),
        'save_txt': load_icon(get_resource_path(os.path.join('assets', 'save2', 'stxt.png'))),
        'save_xml': load_icon(get_resource_path(os.path.join('assets', 'save2', 'sxml.png'))),
    }

    btn_name = {
        'save_word': 'Сохранить как Word',
        'save_excel': 'Сохранить как Excel',
        'save_pdf': 'Сохранить как PDF',
        'save_csv': 'Сохранить как CSV',
        'save_json': 'Сохранить как JSON',
        'save_html': 'Сохранить как HTML',
        'save_txt': 'Сохранить как TXT',
        'save_xml': 'Сохранить как XML',
    }
    return {
        'icons': icons,
        'saves_icons': saves_icons,
        'btn_names': btn_name,
    }


# def main() -> None:
#     """
#     Main function.
#     :return: None
#     """
#     app = QApplication(sys.argv)
#     assets = configurate_assets()
#
#     main_window = Ui_StartMenu(assets)
#
#     try:
#         if len(sys.argv) > 1:
#             file_path = sys.argv[1]
#             if not file_path.endswith('.mdth'):
#                 QMessageBox.critical(None, "Error", "Этот файл невозможно открыть")
#                 sys.exit(1)
#             main_window.open_main_window(file_path, from_file=True)
#         else:
#             main_window.show()
#
#         sys.exit(app.exec())
#
#     except Exception as e:
#         QMessageBox.critical(None, "Error", str(e))
#         sys.exit(1)
#
def main() -> None:
    """
    Main function.
    :return: None
    """
    app = QApplication(sys.argv)
    assets = configurate_assets()

    splash_screen = SplashScreen(os.path.join(EXE_DIR, os.path.join('assets', 'start_screen.gif')))
    splash_screen.show()
    splash_screen.start()

    main_window = Ui_StartMenu(assets)

    try:
        if len(sys.argv) > 1:
            file_path = sys.argv[1]
            if not file_path.endswith('.mdth'):
                QMessageBox.critical(None, "Error", "Этот файл невозможно открыть")
                sys.exit(1)
            splash_screen.finished.connect(lambda: main_window.open_main_window(file_path, from_file=True))
        else:
            splash_screen.finished.connect(main_window.show)

        sys.exit(app.exec())

    except Exception as e:
        QMessageBox.critical(None, "Error", str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
