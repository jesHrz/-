# -*- mode: python -*-

block_cipher = None


a = Analysis(['run.py'],
             pathex=['E:\\Program\\Python\\SDU-classAssistant\\v3'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          version='version.txt',
          icon='icon\\favicon.ico',
          name='run',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
