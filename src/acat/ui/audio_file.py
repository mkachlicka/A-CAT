import pathlib
from dataclasses import dataclass, field
from typing import NamedTuple

from pydub import AudioSegment


class PraatScore(NamedTuple):
    comprehensibility: float
    nativelikeness: float


@dataclass
class AudioFileInfo:
    path: pathlib.Path
    score: PraatScore | None = field(default=None)
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

    @property
    def comprehensibility(self) -> float | None:
        if self.score:
            return self.score.comprehensibility
        return None

    @property
    def nativelikeness(self) -> float | None:
        if self.score:
            return self.score.nativelikeness
        return None

    @property
    def comprehensibility_str(self) -> str:
        if self.comprehensibility:
            return f"{self.comprehensibility:.2f}"
        return "N/A"

    @property
    def nativelikeness_str(self) -> str:
        if self.nativelikeness:
            return f"{self.nativelikeness:.2f}"
        return "N/A"
