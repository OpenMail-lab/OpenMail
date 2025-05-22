from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Collect all required data files
datas = collect_data_files('frontend')
datas += collect_data_files('backend')
datas += collect_data_files('assets')

# Collect all submodules
hiddenimports = collect_submodules('customtkinter')
hiddenimports += ['webview', 'PIL', 'tkinter']
