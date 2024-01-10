from pathlib import Path

import PyInstaller.__main__

HERE = Path(__file__).parent.absolute()
path_to_main = str(HERE / "__main__.py")


def build_test():
    PyInstaller.__main__.run(
        [
            path_to_main,
            "--onefile",
            "--windowed",
            "--onedir",
            "-y",
            "--log-level=DEBUG",
            "--clean",
        ]
    )
