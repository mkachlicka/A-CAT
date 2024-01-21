from acat.backend.utils import bind_ffmpeg
from acat.ui import start_application


def main() -> None:
    bind_ffmpeg()
    start_application()
