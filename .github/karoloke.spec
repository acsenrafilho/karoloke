# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file for Karoloke
# This file configures how PyInstaller bundles the application into a single executable

block_cipher = None

a = Analysis(
    ['../karoloke/start_karaoke.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('../karoloke/templates', 'karoloke/templates'),
        ('../karoloke/static', 'karoloke/static'),
        ('../karoloke/backgrounds', 'karoloke/backgrounds'),
    ],
    hiddenimports=[
        'flask',
        'jinja2',
        'qrcode',
        'PIL',
        'pydantic',
        'dotenv',
        'rich',
    ],
    hookspath=[],
    hooksconfig={},
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='karoloke',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Set to False for windowed mode (no console)
    disable_windowing_fallback=False,
    icon='../docs/assets/karoloke-icon.ico',  # Windows/Linux icon
)
