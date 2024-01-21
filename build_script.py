import os
import pathlib
import sys
from pathlib import Path
from typing import Generator, List

import PyInstaller.__main__
from acat.backend.utils import get_praat_func_dir

HERE = Path(__file__).parent.absolute()
PACKAGE = HERE / "src" / "acat"

path_to_main = str(PACKAGE / "__main__.py")


def _praat_resource_path() -> List[str]:
    praat_func_path = get_praat_func_dir()
    mapping = [
        (str(praat_func.absolute()), f"praat/")
        for praat_func in praat_func_path.iterdir()
    ]

    return [f"--add-data={path}:{package}" for path, package in mapping]


def _ffmpeg_resource_path() -> Generator[str, None, None]:
    ffmpeg_path = os.environ.get("_ACAT_FFMPEG_PATH", "")
    ffmpeg_path = pathlib.Path(ffmpeg_path)

    if ffmpeg_path.is_dir():
        if sys.platform == "darwin" or sys.platform == "linux":
            ffmpeg_path = ffmpeg_path / "ffmpeg"
        elif sys.platform == "win32":
            ffmpeg_path = ffmpeg_path / "ffmpeg.exe"
        else:
            raise NotImplementedError(f"Unsupported platform: {sys.platform}")

    if not ffmpeg_path.exists():
        raise FileNotFoundError(f"ffmpeg not found at {ffmpeg_path}")

    ffmpeg_path = ffmpeg_path.absolute()

    if ffmpeg_path is not None:
        yield f"--add-binary={ffmpeg_path}:bin/"


def test_build(log_level: str = "DEBUG"):
    PyInstaller.__main__.run(
        [
            path_to_main,
            "--name=ACAT",
            "--onefile",
            "--windowed",
            "--onedir",
            "-y",
            f"--log-level={log_level}",
            "--clean",
            "--icon=ACAT_ICON.png",
            *_praat_resource_path(),
            *_ffmpeg_resource_path(),
        ]
    )
