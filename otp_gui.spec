# otp_gui.spec (optional)
block_cipher = None

a = Analysis(
    ['otp_gui.py'],
    pathex=[],
    binaries=[],
    datas=[('qr_code.png', '.'), ('secret.key', '.')],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='otp_gui',
    debug=False,
    strip=False,
    upx=True,
    console=False  # Set to False to hide terminal window
)
