import pathlib
from dataclasses import dataclass, field

from pydub import AudioSegment


@dataclass
class AudioFileInfo:
    path: pathlib.Path
    score: float | None = field(default=None)
    audio: str | None = field(default=None, init=False)

    def __post_init__(self) -> None:
        self.audio = AudioSegment.from_file(self.path)

    @property
    def extension(self) -> str:
        return self.path.suffix

    @property
    def file_name(self) -> str:
        return self.path.stem

    @property
    def audio_length(self) -> float:
        return len(self.audio) / 1000.0

    @property
    def audio_length_str(self) -> str:
        return f"{self.audio_length:.2f} s"
