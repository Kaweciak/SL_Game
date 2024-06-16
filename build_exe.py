import PyInstaller.__main__

PyInstaller.__main__.run([
    '--name=%s' % 'game',
    '--onefile',
    '--windowed',
    '--add-data=%s' % 'Levels;Levels',
    '--add-data=%s' % 'README.md;.',
    'main_menu.py',
])
