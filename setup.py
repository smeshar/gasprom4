from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but they might need fine-tuning.
build_exe_options = {
    "includes": ["colorama", "plotext", "key_generator"],
    "include_files": ["buy.wav", "buy2.wav", "elec.wav", "load.wav", "save.wav", "sell.wav", "shop.wav"],
    "packages": ["pymysql"]
}

setup(
    name="Gasprom",
    version="2.1",
    description="Gapsrom crypto game",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py")]
)