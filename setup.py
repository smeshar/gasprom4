from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but they might need fine-tuning.
build_exe_options = {
    "includes": ["colorama", "plotext", "key_generator"],
    "include_files": ["buy2.wav", "sell.wav", "shop.wav"],
    "packages": ["pymysql"]
}

setup(
    name="Gasprom",
    version="2.1.4",
    description="Gasprom crypto game",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py")]
)