# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from pathlib import Path
from PyInstaller.utils.hooks import collect_submodules, collect_dynamic_libs

block_cipher = None

project_root = Path(os.getcwd())

binaries = []
for package in ("PyQt5", "numpy", "scipy", "sklearn", "pyproj", "PIL", "shapely"):
    try:
        binaries += collect_dynamic_libs(package)
    except Exception:
        pass

library_bin = Path(os.environ.get("CONDA_PREFIX", sys.prefix)) / "Library" / "bin"
if library_bin.exists():
    for dll_path in library_bin.glob('*.dll'):
        binaries.append((str(dll_path), '.'))

library_plugins = library_bin / 'plugins'
if library_plugins.exists():
    for file_path in library_plugins.rglob('*'):
        if file_path.is_file():
            relative_target = Path('plugins') / file_path.relative_to(library_plugins)
            binaries.append((str(file_path), str(relative_target)))

datas = []
for folder in ("img", "fonts", "resources", "georgia"):
    folder_path = project_root / folder
    if folder_path.exists():
        for file_path in folder_path.rglob('*'):
            if file_path.is_file():
                relative_target = Path(folder) / file_path.relative_to(folder_path).parent
                datas.append((str(file_path), str(relative_target)))

hiddenimports = collect_submodules("mgwrlib")

a = Analysis(
    ['main.py'],
    pathex=[str(project_root)],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='MGWR-GUI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(project_root / 'resources' / 'img' / 'MGWR-pc.ico')
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='MGWR-GUI',
)
