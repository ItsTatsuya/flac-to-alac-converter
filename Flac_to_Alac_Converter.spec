# -*- mode: python ; coding: utf-8 -*-
import os
import site
from pathlib import Path

# Define paths
PYTHON_PATH = r'C:\Users\Tatsuya\AppData\Local\Programs\Python\Python313'
SITE_PACKAGES = os.path.join(PYTHON_PATH, 'Lib', 'site-packages')
TKDND_PATH = os.path.join(SITE_PACKAGES, 'tkinterdnd2', 'tkdnd', 'win-x64')

a = Analysis(
    ['src\\gui.py'],
    pathex=[],
    binaries=[
        (os.path.join(PYTHON_PATH, 'python313.dll'), '.')
    ],
    datas=[
        (TKDND_PATH, 'tkdnd'),
        (os.path.join(SITE_PACKAGES, 'tkinterdnd2'), 'tkinterdnd2')
    ],
    hiddenimports=['tkinterdnd2'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Flac_to_Alac_Converter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['converter.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Flac_to_Alac_Converter',
)
