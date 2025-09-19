# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path
from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs

block_cipher = None

project_root = Path.cwd()


def dedupe(items):
    seen = set()
    unique = []
    for src, dest in items:
        key = (src, dest)
        if key not in seen:
            unique.append((src, dest))
            seen.add(key)
    return unique


def safe_collect(collector, package, **kwargs):
    try:
        return collector(package, **kwargs)
    except ImportError:
        return []


datas = []

img_dir = project_root / "img"
if img_dir.exists():
    datas.append((str(img_dir), "img"))

font_file = project_root / "fonts" / "arial.ttf"
if font_file.exists():
    datas.append((str(font_file), "fonts"))

# Library data that is required at runtime but not imported directly.
datas.extend(safe_collect(collect_data_files, "pyproj", excludes=["test*", "tests*"]))
datas.extend(safe_collect(collect_data_files, "spglm", excludes=["test*", "tests*"]))
datas.extend(safe_collect(collect_data_files, "spreg", excludes=["test*", "tests*"]))
datas.extend(safe_collect(collect_data_files, "libpysal", excludes=["examples*", "tests*"]))
datas = dedupe(datas)

binaries = []
binaries.extend(safe_collect(collect_dynamic_libs, "pyproj"))
binaries.extend(safe_collect(collect_dynamic_libs, "shapely"))
binaries.extend(safe_collect(collect_dynamic_libs, "spglm"))
binaries.extend(safe_collect(collect_dynamic_libs, "spreg"))
binaries.extend(safe_collect(collect_dynamic_libs, "libpysal"))
binaries = dedupe(binaries)

hiddenimports = [
    "shapely.speedups._speedups",
    "sklearn.utils._weight_vector",
    "sklearn.utils._typedefs",
]

excludes = [
    "lib2to3.tests",
    "email.tests",
    "pydoc_data",
    "numpy.random._examples",
    "tkinter.test",
]

a = Analysis(
    ["main.py"],
    pathex=[str(project_root)],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
    optimize=1,
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher,
)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="MGWR",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon='resources/img/MGWR-pc.ico'
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name="MGWR",
)
