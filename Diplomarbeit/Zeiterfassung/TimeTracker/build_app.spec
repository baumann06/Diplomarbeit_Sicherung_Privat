# -*- mode: python ; coding: utf-8 -*-

# TimeTracker Pro - PyInstaller Specification File
# Für eine professionelle Desktop-Anwendung

block_cipher = None

a = Analysis(
    ['time_tracker_working.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('logo.png', '.'),  # Logo mit einpacken
        ('requirements.txt', '.'),  # Requirements für Referenz
    ],
    hiddenimports=[
        'PIL',
        'PIL._tkinter_finder',
        'tkinter',
        'sqlite3',
        'plotly',
        'pandas'
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
    name='TimeTracker_Pro',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Keine Konsole anzeigen
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='logo.png'  # App-Icon
)
