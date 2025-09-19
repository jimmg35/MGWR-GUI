# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

import ctypes
import multiprocessing as mp
import os
import sys
import time
from pathlib import Path

import psutil
from PyQt5 import QtCore, QtGui, QtWidgets

from src.gui import Ui_Dialog


def _ensure_streams() -> None:
    """Redirect stdout/stderr to devnull when running without consoles."""
    if not sys.stdout:
        sys.stdout = open(os.devnull, "w")
    if not sys.stderr:
        sys.stderr = open(os.devnull, "w")


def _configure_high_dpi() -> None:
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)  # Windows 8.1+
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()  # Windows 7
        except Exception:
            pass

    if hasattr(QtCore.Qt, "AA_EnableHighDpiScaling"):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, "AA_UseHighDpiPixmaps"):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


def resource_path(relative_path: str) -> str:
    search_roots = []
    if hasattr(sys, "_MEIPASS"):
        base = Path(sys._MEIPASS)
        search_roots.extend([base, base / "_internal"])

    module_dir = Path(__file__).resolve().parent
    search_roots.extend(
        [
            module_dir,
            module_dir / "_internal",
            module_dir.parent,
            module_dir.parent / "_internal",
        ]
    )

    executable_dir = Path(sys.argv[0]).resolve().parent
    search_roots.extend([executable_dir, executable_dir / "_internal"])

    cwd = Path.cwd()
    search_roots.extend([cwd, cwd / "_internal"])

    for base in search_roots:
        candidate = base / relative_path
        if candidate.exists():
            return str(candidate)
    return str(module_dir / relative_path)


def _load_custom_font(app: QtWidgets.QApplication) -> None:
    font_path = resource_path("fonts/arial.ttf")
    font_id = QtGui.QFontDatabase.addApplicationFont(font_path)
    if font_id == -1:
        print("failed to load font:", font_path)
        return

    font_families = QtGui.QFontDatabase.applicationFontFamilies(font_id)
    if not font_families:
        return

    font = QtGui.QFont(font_families[0])
    font.setPointSize(10)
    app.setFont(font)
    print(f"font {font_families[0]} has been loaded successfully")


def run() -> int:
    mp.freeze_support()
    _ensure_streams()
    _configure_high_dpi()

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("mac")

    _load_custom_font(app)

    screen = app.primaryScreen()
    scale_factor = screen.size().width() / 1920.0

    font = app.font()
    font.setHintingPreference(QtGui.QFont.PreferFullHinting)
    app.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)
    app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    font.setPointSizeF(font.pointSizeF() * scale_factor)
    app.setFont(font)

    app_icon = QtGui.QIcon()
    app_icon.addFile(resource_path("img/MGWR16.png"), QtCore.QSize(16, 16))
    app_icon.addFile(resource_path("img/MGWR24.png"), QtCore.QSize(24, 24))
    app_icon.addFile(resource_path("img/MGWR32.png"), QtCore.QSize(32, 32))
    app_icon.addFile(resource_path("img/MGWR48.png"), QtCore.QSize(48, 48))
    app_icon.addFile(resource_path("img/MGWR64.png"), QtCore.QSize(64, 64))
    app_icon.addFile(resource_path("img/MGWR128.png"), QtCore.QSize(128, 128))
    app.setWindowIcon(app_icon)

    print(resource_path("img/Group.png"))
    splash_pix = QtGui.QPixmap(resource_path("img/Group.png"))

    splash = QtWidgets.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
    progress_bar = QtWidgets.QProgressBar(splash)
    margin = splash.height() // 20
    progress_bar.setGeometry(
        splash.width() // 10,
        9 * splash.height() // 10 - margin,
        8 * splash.width() // 10,
        splash.height() // 10,
    )

    splash.setMask(splash_pix.mask())
    splash.show()
    for i in range(0, 100):
        progress_bar.setValue(i)
        target = time.time() + 0.01
        while time.time() < target:
            app.processEvents()

    dialog = QtWidgets.QDialog()
    dialog.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowCloseButtonHint)
    ui = Ui_Dialog()
    pool = mp.Pool(psutil.cpu_count())
    ui.setupUi(dialog, pool)
    ui.scaleUi(dialog, scale_factor)
    dialog.setFixedSize(dialog.size())
    ui.addActionsToUI()
    dialog.show()
    splash.finish(dialog)

    try:
        return app.exec_()
    finally:
        pool.close()
        pool.join()


def main() -> int:
    return run()


if __name__ == "__main__":
    sys.exit(main())
